from boto3.dynamodb.conditions import Key, Attr, Contains


def get_user_filters(data):
    filters = None

    for key, value in data.items():
        filter_value = filters and value

        if filter_value:
            if key == "date":
                filters &= Attr("created_at").begins_with(value)
            elif key == "is_active":
                filters &= Attr(key).eq(value)
            else:
                filters &= Attr(key).contains(value)
        elif value is not None:
            if key == "date":
                filters = Attr("created_at").begins_with(value)
            elif key == "is_active":
                filters = Attr(key).eq(value)
            else:
                filters = Attr(key).contains(value)

    return filters
