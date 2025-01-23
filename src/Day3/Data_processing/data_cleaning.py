def remove_duplicates(data):
    new_list=list(set(data))
    new_list.sort()
    return print(f"New List Without Duplicates is:{new_list}")    