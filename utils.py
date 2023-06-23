def format_data(data_list):
    formatted_string = "FirstName\n"
    for item in data_list:
        first_name, id_number = item
        formatted_string += f"<a href='tg://user?id={id_number}" \
                            f"'>{first_name}</a>\n\n"
    return formatted_string
