import networkx as nx
import numpy as np


class GenericGraph:

	def __init__(self, graph: nx.Graph = None,
	             types: list = [int, float, complex, str]) -> None:
		"""
		Creates a new generic directed Graph.
		Can accept parameters to specify data to be added before

		:param graph: A pre-existing networkX graph to be used
			as the basis of the new graph.
			If left blank, creates a new graph
		:param types: A list containing all allowed types for nodes
		"""

		self._graph = None
		self.types = types

		if graph is not None:
			self._graph = graph
		else:
			self._graph = nx.Graph()

	def set_graph(self, graph: nx.Graph) -> None:
		"""
		Sets the graph to be used by the graph object

		:param graph: The graph to be used by the graph object
		:return: None
		"""
		self._graph = graph

	def clear_graph(self) -> None:
		"""
		Clears the graph

		"""
		self._graph = None

	def get_graph(self) -> nx.Graph:

		return self._graph

	def compose(self, other_graph: nx.Graph) -> None:
		"""
		Sets the current graph to the composition of other_graph
		with the current graph

		:param other_graph: The graph to be unioned with the current graph
		:return: None
		"""

		if other_graph is not None:
			self._graph = nx.compose(self._graph, other_graph)

	def remove(self, other_graph: nx.Graph) -> None:
		"""
		Sets the current graph to the difference of other_graph
		with the current graph

		:param other_graph: The graph to be subtracted from the current graph
		:return: None
		"""

		if other_graph is not None:
			self._graph = nx.difference(self._graph, other_graph)

	# region Nodes
	def add_node(self, value, **attr) -> bool:
		"""
		Safely adds a node to the graph
		Returns True if the node was added
		:param value:
		:param attr:
		:return:
		"""
		if not self.is_valid_type(type(value)):
			return False

		self._graph.add_node(value, **attr)

	def add_nodes_from(self, values: list, **attr) -> bool:
		"""
		Adds all nodes enumerated with values with the given attributes applied
		If any value is incompatible with the types, the changes will roll back
		Returns True if the nodes were added
		:param values:
		:param attr:
		:return:
		"""
		temp_list_of_nodes = []
		success = True
		for val in values:
			temp_list_of_nodes += val
			success = self.add_node(val, **attr)
			if not success:
				temp_list_of_nodes.remove(val)
				break

		if not success:
			self.remove_nodes_from(temp_list_of_nodes)
			return False
		return True

	def add_nodes_from_anyways(self, values: list, **attr) -> bool:
		"""
		Adds all the nodes from the enumerated values
		No Rollback
		If the node is incompatible, it is skipped
		Returns True if all the nodes were added
		:param values:
		:param attr:
		:return:
		"""
		success = True
		for val in values:
			success = success and self.add_node(val, **attr)

		return success

	def remove_node(self, value) -> bool:
		"""
		Removes a node from the graph
		Returns True if the node was successfully removed
		:param value:
		:return:
		"""
		try:
			self._graph.remove_node(value)
			return True
		except:
			return False

	def remove_nodes_from(self, values: list) -> bool:
		"""
		Removes all the nodes enumerated if the graph contains them
		Returns True if all nodes were successfully removed
		:param values:
		:return:
		"""
		graph_contains_all = True
		for val in values:
			if val not in self._graph:
				graph_contains_all = False
				break

		self._graph.remove_nodes_from(values)
		return graph_contains_all

	def get_node_data(self, property, default=None) -> list:
		"""
		Returns the value specified by 'property' for all the nodes
		Returns the default for any node without the specified property
		:param property:
		:param default:
		:return:
		"""
		return self._graph.nodes.data(property, default=default)

	def get_nodes(self) -> nx.Graph:
		return self._graph.nodes

	def get_neighbors_of(self, node) -> list:
		if node in self._graph:
			return self._graph.neighbors(node)
		return []

	def get_neighborhood_of(self, node, distance=1):
		pass

	# end region

	# region Edges

	def add_edge(self, u_of_edge, v_of_edge, directed:bool = True, **attr) -> bool:
		"""
		Adds an edge to a graph
		If u or v is not an already specified node, it is automatically created
		If u or v is incompatible, the edge is not added
		Returns True if the edge is added
		:param u_of_edge:
		:param v_of_edge:
		:param attr:
		:return:
		"""
		success = True
		if u_of_edge not in self._graph:
			success = success and self.add_node(u_of_edge)
		if success and v_of_edge not in self._graph:
			success = success and self.add_node(v_of_edge)
		if success:
			self._graph.add_edge(u_of_edge, v_of_edge, **attr)
			if not directed:
				self._graph.add_edge(v_of_edge, u_of_edge, **attr)
		return success

	def add_edges_from(self, edges: list, directed: bool = True, **attr) -> bool:
		"""
		Adds all the edges enumerated in the list
		If the data type is incompatible with the graph, changes roll back
		Returns True if all edges are successfully added
		:param edges:
		:param attr:
		:return:
		"""
		temp_list_of_edges = []
		existing_nodes = list(self._graph.nodes)
		success = True
		for edge in edges:
			if len(edge) >= 2:
				temp_list_of_edges += edge
				success = self.add_edge(edge[0],edge[1], directed=directed **attr)
				if not success:
					temp_list_of_edges.remove(edge)
					break
			else:
				success = False
				break

		if not success:
			for edge in temp_list_of_edges:
				self._graph.remove_edge(edge[0], edge[1])
			self._graph.remove_nodes_from(self._graph.nodes - existing_nodes)

	def add_edges_from_anyways(self, edges: list, directed: bool = True, **attr) -> bool:
		"""
		Adds all compatible edges enumerated in the list
		No rollback
		Ignores incompatible edges
		:param edges:
		:param attr:
		:return:
		"""
		success = True
		for edge in edges:
			if len(edge) >= 2:
				success = success and self.add_edge(edge[0],edge[1], directed=directed **attr)
			else:
				success = False
		return success

	def remove_edge(self, u_of_edge, v_of_edge) -> bool:
		try:
			self._graph.remove_edge(u_of_edge, v_of_edge)
			return True
		except nx.NetworkXError:
			return False

	def remove_edges_from(self, edges:list, directed=True) -> bool:
		graph_contains_all = True
		for edge in edges:

			if len(edge) < 2 or not self._graph.has_edge(edge[0], edge[1]):
				graph_contains_all = False

		self._graph.remove_edges_from(edges)
		if not directed:
			edges = [(e[1], e[0]) for e in edges if len(e) >= 2]
			self._graph.remove_edges_from(edges)
		return graph_contains_all

	def get_edge(self, u, v) -> dict:
		try:
			return self._graph[u][v]
		except:
			return None


	# end region

	def is_valid_type(self, tested_type: type) -> bool:
		"""
		A boolean specifying if an object type is supported by the graph
		:param tested_type:
		:return:
		"""
		return tested_type in self.types

	def __contains__(self, item):
		return self.is_valid_type(item) and item in self._graph

	def __len__(self):
		return len(self._graph)
