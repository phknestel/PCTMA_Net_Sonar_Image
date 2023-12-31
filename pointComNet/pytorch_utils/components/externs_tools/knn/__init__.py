from typing import Optional
import os
import torch

_build = "lib/python3.7/site-packages/knn-2.0.0-py3.7-linux-x86_64.egg/knn.so"
_path = os.path.join(os.path.join(os.path.dirname(__file__)), "../../../extensions_build/knn", _build)
torch.ops.load_library(_path)


def knn(x: torch.Tensor, y: torch.Tensor, k: int,
        batch_x: Optional[torch.Tensor] = None,
        batch_y: Optional[torch.Tensor] = None, cosine: bool = False,
        num_workers: int = 1) -> torch.Tensor:
    r"""Finds for each element in :obj:`y` the :obj:`k` nearest points in
    :obj:`x`.

    Args:
        x (Tensor): Node feature matrix
            :math:`\mathbf{X} \in \mathbb{R}^{N \times F}`.
        y (Tensor): Node feature matrix
            :math:`\mathbf{X} \in \mathbb{R}^{M \times F}`.
        k (int): The number of neighbors.
        batch_x (LongTensor, optional): Batch vector
            :math:`\mathbf{b} \in {\{ 0, \ldots, B-1\}}^N`, which assigns each
            node to a specific example. :obj:`batch_x` needs to be sorted.
            (default: :obj:`None`)
        batch_y (LongTensor, optional): Batch vector
            :math:`\mathbf{b} \in {\{ 0, \ldots, B-1\}}^M`, which assigns each
            node to a specific example. :obj:`batch_y` needs to be sorted.
            (default: :obj:`None`)
        cosine (boolean, optional): If :obj:`True`, will use the Cosine
            distance instead of the Euclidean distance to find nearest
            neighbors. (default: :obj:`False`)
        num_workers (int): Number of workers to use for computation. Has no
            effect in case :obj:`batch_x` or :obj:`batch_y` is not
            :obj:`None`, or the input lies on the GPU. (default: :obj:`1`)

    :rtype: :class:`LongTensor`

    .. code-block:: python

        import torch
        from torch_cluster import knn

        x = torch.Tensor([[-1, -1], [-1, 1], [1, -1], [1, 1]])
        batch_x = torch.tensor([0, 0, 0, 0])
        y = torch.Tensor([[-1, 0], [1, 0]])
        batch_y = torch.tensor([0, 0])
        assign_index = knn(x, y, 2, batch_x, batch_y)
    """

    x = x.view(-1, 1) if x.dim() == 1 else x
    y = y.view(-1, 1) if y.dim() == 1 else y
    x, y = x.contiguous(), y.contiguous()

    ptr_x: Optional[torch.Tensor] = None
    if batch_x is not None:
        assert x.size(0) == batch_x.numel()
        batch_size = int(batch_x.max()) + 1

        deg = x.new_zeros(batch_size, dtype=torch.long)
        deg.scatter_add_(0, batch_x, torch.ones_like(batch_x))

        ptr_x = deg.new_zeros(batch_size + 1)
        torch.cumsum(deg, 0, out=ptr_x[1:])

    ptr_y: Optional[torch.Tensor] = None
    if batch_y is not None:
        assert y.size(0) == batch_y.numel()
        batch_size = int(batch_y.max()) + 1

        deg = y.new_zeros(batch_size, dtype=torch.long)
        deg.scatter_add_(0, batch_y, torch.ones_like(batch_y))

        ptr_y = deg.new_zeros(batch_size + 1)
        torch.cumsum(deg, 0, out=ptr_y[1:])

    return torch.ops.my_torch_cluster.knn(x, y, ptr_x, ptr_y, k, cosine, num_workers)


def knn_graph(x: torch.Tensor, k: int, batch: Optional[torch.Tensor] = None,
              loop: bool = False, flow: str = 'source_to_target',
              cosine: bool = False, num_workers: int = 1) -> torch.Tensor:
    r"""Computes graph edges to the nearest :obj:`k` points.

    Args:
        x (Tensor): Node feature matrix
            :math:`\mathbf{X} \in \mathbb{R}^{N \times F}`.
        k (int): The number of neighbors.
        batch (LongTensor, optional): Batch vector
            :math:`\mathbf{b} \in {\{ 0, \ldots, B-1\}}^N`, which assigns each
            node to a specific example. :obj:`batch` needs to be sorted.
            (default: :obj:`None`)
        loop (bool, optional): If :obj:`True`, the graph will contain
            self-loops. (default: :obj:`False`)
        flow (string, optional): The flow direction when used in combination
            with message passing (:obj:`"source_to_target"` or
            :obj:`"target_to_source"`). (default: :obj:`"source_to_target"`)
        cosine (boolean, optional): If :obj:`True`, will use the Cosine
            distance instead of Euclidean distance to find nearest neighbors.
            (default: :obj:`False`)
        num_workers (int): Number of workers to use for computation. Has no
            effect in case :obj:`batch` is not :obj:`None`, or the input lies
            on the GPU. (default: :obj:`1`)

    :rtype: :class:`LongTensor`

    .. code-block:: python

        import torch
        from torch_cluster import knn_graph

        x = torch.Tensor([[-1, -1], [-1, 1], [1, -1], [1, 1]])
        batch = torch.tensor([0, 0, 0, 0])
        edge_index = knn_graph(x, k=2, batch=batch, loop=False)
    """

    assert flow in ['source_to_target', 'target_to_source']
    edge_index = knn(x, x, k if loop else k + 1, batch, batch, cosine,
                     num_workers)

    if flow == 'source_to_target':
        row, col = edge_index[1], edge_index[0]
    else:
        row, col = edge_index[0], edge_index[1]

    if not loop:
        mask = row != col
        row, col = row[mask], col[mask]

    return torch.stack([row, col], dim=0)
