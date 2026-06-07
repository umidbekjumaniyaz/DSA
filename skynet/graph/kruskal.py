"""Kruskal's Minimum Spanning Tree algorithm implementation."""

from typing import Dict, List, Optional, Set

from skynet.graph.mst_base import MSTAlgorithm, MSTResult
from skynet.graph.union_find import UnionFind
from skynet.graph.weighted_graph import WeightedGraph


class KruskalMST(MSTAlgorithm):
    """Kruskal's MST algorithm using edge sorting and Union-Find cycle detection.

    Builds the MST by processing edges in ascending weight order and adding
    each edge that does not create a cycle (detected via Union-Find). This
    greedy approach guarantees a minimum spanning tree for connected graphs.
    """

    def compute_mst(self, graph: WeightedGraph, start_node: Optional[str] = None) -> MSTResult:
        """Compute MST using Kruskal's algorithm.

        Sorts all edges by weight and greedily selects edges that do not
        form cycles using Union-Find. The start_node parameter is accepted
        but ignored since Kruskal's algorithm does not require a starting node.

        Args:
            graph: The weighted graph to compute the MST for.
            start_node: Ignored. Kruskal's does not need a start node.

        Returns:
            MSTResult with the MST edges and total cost, or a failure result
            if the graph has fewer than 2 nodes or is disconnected.
        """
        nodes = graph.get_all_nodes()
        num_nodes = len(nodes)

        # Handle graph with fewer than 2 nodes
        if num_nodes < 2:
            return MSTResult(
                success=False,
                edges=[],
                total_cost=0,
                message="Insufficient nodes to form a spanning tree.",
            )

        # Step 1: Get all edges and sort by weight ascending
        all_edges = graph.get_all_edges()
        sorted_edges = sorted(all_edges, key=lambda edge: edge[2])

        # Step 2: Create Union-Find with all nodes
        uf = UnionFind()
        for node in nodes:
            uf.make_set(node)

        # Step 3: Greedily select edges that don't form cycles
        mst_edges: List[tuple] = []
        total_cost = 0

        for src, dest, weight in sorted_edges:
            if uf.find(src) != uf.find(dest):
                uf.union(src, dest)
                mst_edges.append((src, dest, weight))
                total_cost += weight

                # If MST has V-1 edges, we're done
                if len(mst_edges) == num_nodes - 1:
                    break

        # Step 4: Check if graph is disconnected (MST has < V-1 edges)
        if len(mst_edges) < num_nodes - 1:
            # Find components using Union-Find structure
            components = self._find_components(nodes, uf)
            component_strs = [
                "{" + ",".join(sorted(component)) + "}"
                for component in components
            ]
            components_display = ", ".join(component_strs)

            return MSTResult(
                success=False,
                edges=mst_edges,
                total_cost=total_cost,
                message=f"Graph is disconnected. Components: {components_display}",
            )

        return MSTResult(
            success=True,
            edges=mst_edges,
            total_cost=total_cost,
            message=f"MST computed successfully using Kruskal's algorithm. Total cost: {total_cost}",
        )

    def get_name(self) -> str:
        """Return the name of this algorithm.

        Returns:
            A string identifying this as Kruskal's Algorithm.
        """
        return "Kruskal's Algorithm"

    def _find_components(self, nodes: List[str], uf: UnionFind) -> List[Set[str]]:
        """Find disconnected components using the Union-Find structure.

        Groups nodes by their root representative to identify connected components.

        Args:
            nodes: List of all node identifiers in the graph.
            uf: The Union-Find structure after edge processing.

        Returns:
            List of sets, each containing the nodes in one connected component.
        """
        component_map: Dict[str, Set[str]] = {}
        for node in nodes:
            root = uf.find(node)
            if root not in component_map:
                component_map[root] = set()
            component_map[root].add(node)

        return list(component_map.values())
