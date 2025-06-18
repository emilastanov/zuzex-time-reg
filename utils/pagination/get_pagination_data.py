def get_pagination_data(total_count, limit, page_number):
    limit = int(limit)
    total_count = int(total_count)
    page_number = int(page_number)

    total_pages = (total_count + limit - 1) // limit
    offset = (page_number - 1) * limit
    next_page = page_number + 1 if page_number + 1 <= total_pages else None
    prev_page = page_number - 1 if page_number - 1 > 0 else None

    return {
        "limit": limit,
        "offset": offset,
        "total_count": total_count,
        "current_page": page_number,
        "next_page": next_page,
        "prev_page": prev_page,
        "total_pages": total_pages,
    }
