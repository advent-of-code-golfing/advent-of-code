from src.utils import get_input_filename


def load_data(filename: str) -> dict:
    conn_list = list()
    with open(filename, "r") as f:
        for line in f.readlines():
            coms = [x for x in line.strip("\n").split("-")]
            conn_list.append(coms)

    conn_dict = dict()
    for coms in conn_list:
        com_1, com_2 = coms[0], coms[1]

        if com_1 in conn_dict:
            conn_dict[com_1].append(com_2)
        else:
            conn_dict[com_1] = [com_2]
        if com_2 in conn_dict:
            conn_dict[com_2].append(com_1)
        else:
            conn_dict[com_2] = [com_1]

    return conn_dict


def q1(
    conn_dict: dict,
) -> int:
    # You can probably make this faster if you sort everything, but it's a bit annoying because
    # t might not be the first sorted one
    keys = list(conn_dict.keys())
    keys.sort()
    num_parties = 0
    for com, com_connections in conn_dict.items():
        if com.startswith("t"):
            num_connections = len(com_connections)
            for i in range(num_connections):
                connection_1 = com_connections[i]
                second_starts_with_t = 0
                if connection_1.startswith("t"):
                    second_starts_with_t = 1
                for j in range(i + 1, num_connections):
                    connection_2 = com_connections[j]
                    third_starts_with_t = 0
                    if connection_2.startswith("t"):
                        third_starts_with_t = 1
                    num_t = 1 + second_starts_with_t + third_starts_with_t
                    if connection_2 in conn_dict[connection_1]:
                        num_parties += 1 / num_t
    return int(num_parties)


def create_sorted_conn_dict(conn_dict: dict) -> tuple:
    """
    return list of all computers sorted +
    in the sorted_conn_dict, each com only contains the list of
    computers connected to it which comes alphabetically afterwards,
    also all sorted
    """
    coms = list(conn_dict.keys())
    coms.sort()
    conn_dict_sorted = dict()

    for com in coms:
        connections = conn_dict[com]
        connections.sort()
        for i, connection in enumerate(connections):
            if connection > com:
                break
        conn_dict_sorted[com] = connections[i:]

    return coms, conn_dict_sorted


def find_largest_subgraph_recursive(
    com_list: list, min_size: int, conn_dict_sorted: dict
) -> tuple:
    """
    Finds maximum complete subgraph in a list, assumes com_list is sorted
    return 0 if we can't find subgraph greater than min_size
    """
    len_com_list = len(com_list)
    if len_com_list < max(1, min_size):
        return 0, ""

    if len_com_list == 2:
        if com_list[1] in conn_dict_sorted[com_list[0]]:
            return 2, com_list[0] + "," + com_list[1]
        else:
            return 0, ""

    connected_to_first = list()
    first_connections = conn_dict_sorted[com_list[0]]
    for com in com_list[1:]:
        if com in first_connections:
            connected_to_first.append(com)

    len_mscf, mscf = find_largest_subgraph_recursive(
        connected_to_first, min_size - 1, conn_dict_sorted
    )
    len_mswf, mswf = find_largest_subgraph_recursive(
        com_list[1:], min_size, conn_dict_sorted
    )

    if len_mscf + 1 >= len_mswf:
        return len_mscf + 1, com_list[0] + "," + mscf
    else:
        return len_mswf, mswf


def q2(conn_dict: dict) -> str:
    com_sorted, conn_dict_sorted = create_sorted_conn_dict(conn_dict)

    # You can actually apply the above function direction on the whole list of keys. But
    # since the longest connection for one computer is 11 vs 500+ computers, I think this is faster
    cur_max_subg_len = 0
    cur_max_subg = ""
    for com in com_sorted:
        len_subg, subg = find_largest_subgraph_recursive(
            conn_dict_sorted[com], cur_max_subg_len - 1, conn_dict_sorted
        )
        if len_subg + 1 > cur_max_subg_len:
            cur_max_subg_len = len_subg + 1
            cur_max_subg = com + "," + subg

    return cur_max_subg


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    conn_dict = load_data(filename)
    print(q1(conn_dict))
    print(q2(conn_dict))
