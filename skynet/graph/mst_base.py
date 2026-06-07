"""Abstract base class and result types for MST algorithm implementations."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class MSTResult:
    """Result of a Minimum Spanning Tree computation.

    Encapsulates the outcome of an MST algorithm execution, including
    the selected edges, total cost, and a descriptive message.

    Attributes:
        success: Whether the MST computation completed successfully.
        edges: List of edges in the MST, each as (source, destination, weight).
        total_cost: The sum of all edge weights in the MST.
        message: A human-readable description of the computation outcome.
    """

    success: bool
    edges: List[Tuple[str, str, int]] = field(default_factory=list)
    total_cost: int = 0
    message: str = ""


class MSTAlgorithm(ABC):
    """Abstract base class for Minimum Spanning Tree algorithms.

    Defines the common interface for MST algorithm implementations
    (Prim's and Kruskal's). Enables polymorphic substitution so that
    either algorithm can be used interchangeably through the same
    interface, fulfilling the OOP polymorphism requirement.
    """

    @abstractmethod
    def compute_mst(self, graph: 'WeightedGraph', start_node: Optional[str] = None) -> MSTResult:
        """Compute the minimum spanning tree of the given graph.

        Args:
            graph: The weighted graph to compute the MST for.
            start_node: Optional starting node for algorithms that require one
                        (e.g., Prim's). May be None for algorithms that don't
                        need a start node (e.g., Kruskal's).

        Returns:
            MSTResult containing the MST edges, total cost, and status.
            If the graph is disconnected, returns a failure result with
            information about the disconnected components.
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the MST algorithm.

        Returns:
            A string identifying this algorithm (e.g., "Prim's Algorithm",
            "Kruskal's Algorithm").
        """
        pass
