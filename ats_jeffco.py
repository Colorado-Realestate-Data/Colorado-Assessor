# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def get_property_data(sch=""):
    """Get property id and return dictionary with data

    Attributes:
    sch: property id

    """
    property_url = "http://ats.jeffco.us/ats/displaygeneral.do?sch={0}".format(sch)
    r = requests.get(property_url)
    property_page = BeautifulSoup(r.text, "lxml")
    property_dict = {}

    # Get data from the single data fields
    data_cells = property_page.find_all("td")
    for i, data_cell in enumerate(data_cells):
        try:
            cell_text = data_cell.text.strip()
            if "PIN/Schedule" in cell_text:
                property_dict["PIN"] = ":".join(cell_text.split(":")[1:]).strip()
            elif "status:" in cell_text:
                property_dict["Status"] = ":".join(cell_text.split(":")[1:]).strip()
            elif "AIN/Parcel ID:" in cell_text:
                property_dict["AIN"] = ":".join(cell_text.split(":")[1:]).strip()
            elif "Property Type:" in cell_text:
                property_dict["property_type"] = ":".join(cell_text.split(":")[1:]).strip()
            elif "Neighborhood:" in cell_text:
                property_dict["neighborhood"] = " ".join(":".join(cell_text.split(":")[1:]).strip().split())
            elif "Subdivision Name:" in cell_text:
                property_dict["subdivision_name"] = ":".join(cell_text.split(":")[1:]).strip()
            elif "Adjusted Year Built:" in cell_text:
                property_dict["adjusted_year_built"] = ":".join(cell_text.split(":")[1:]).strip()
            elif "Year Built:" in cell_text:
                property_dict["year_built"] = ":".join(cell_text.split(":")[1:]).strip()
        except (AttributeError, IndexError):
            continue

    # Define data from tables
    data_tables = property_page.find_all("table")
    for data_table in data_tables:
        try:
            table_header = data_table.find("tr", class_="tableheaders").text
            if "Owner Name(s)" in table_header:
                property_dict["owners"] = parse_one_column_table(data_table)
            elif "Assessor Parcel Maps Associated" in table_header:
                property_dict["Assessor Parcel Maps Associated with Schedule"] = parse_one_column_table(data_table)
            elif "Land Characteristics" in table_header:
                property_dict["land_characteristics"] = parse_one_column_table(data_table)
            elif (
                "Block" in table_header and
                "Lot" in table_header and
                "Key" in table_header
                ):
                property_dict["property_description"] =  parse_many_columns_table(data_table, name="property_description")
            elif (
                "Item" in table_header and
                "Quality" in table_header
                ):
                property_dict["property_inventory_1"] =  parse_many_columns_table(data_table)
            elif (
                "Areas" in table_header and
                "Quality" in table_header
                ):
                property_dict["property_inventory_2"] =  parse_many_columns_table(data_table)
            elif (
                "Adjustment Code" in table_header and
                "Adjustment SqFt" in table_header
                ):
                property_dict["property_inventory_3"] =  parse_many_columns_table(data_table)
            elif (
                "Sale Date" in table_header and
                "Sale Amount" in table_header
                ):
                property_dict["sales_history"] =  parse_many_columns_table(data_table)
            elif (
                "Payable" in table_header and not data_table.table
                ):
                property_dict["tax_information"] =  parse_many_columns_table(data_table, name="tax_info")
            elif (
                "Mill Levy" in table_header and not data_table.table
                ):
                property_dict["mill_levy_information"] =  parse_many_columns_table(data_table, name="mill_levy_information")
        except AttributeError:
            pass

        if "Property Address:" in data_table.text and not data_table.table:
            address_data = parse_address_table(data_table)
            property_dict["property_address"] = address_data[0]
            property_dict["mailing_address"] = address_data[1]

    return property_dict


def get_property_history(sch="", year=""):
    """Get property id and return dictionary with history data

    Attributes:
    sch: property id
    year: year of data

    """
    # Start session and get response from the main page first
    s = requests.Session()
    property_url = "http://ats.jeffco.us/ats/displaygeneral.do?sch={0}".format(sch)
    r = s.get(property_url)
    history_url = "http://ats.jeffco.us/ats/displayhistory.do?sch={0}&year={1}".format(sch, year)
    r = s.get(history_url)
    history_property_page = BeautifulSoup(r.text, "lxml")
    property_dict = {}

    # Get data from the single data fields
    data_cells = history_property_page.find_all("td")
    for i, data_cell in enumerate(data_cells):
        try:
            cell_text = data_cell.text.strip()
            if "PIN/Schedule" in cell_text:
                property_dict["PIN"] = ":".join(cell_text.split(":")[1:]).strip()
            elif "status:" in cell_text:
                property_dict["Status"] = ":".join(cell_text.split(":")[1:]).strip()
            elif "AIN/Parcel ID:" in cell_text:
                property_dict["AIN"] = ":".join(cell_text.split(":")[1:]).strip()
            elif "Property Type:" in cell_text:
                property_dict["property_type"] = ":".join(cell_text.split(":")[1:]).strip()
            elif "Neighborhood:" in cell_text:
                property_dict["neighborhood"] = " ".join(":".join(cell_text.split(":")[1:]).strip().split())
            elif "Subdivision Name:" in cell_text:
                property_dict["subdivision_name"] = ":".join(cell_text.split(":")[1:]).strip()
            elif "Adjusted Year Built:" in cell_text:
                property_dict["adjusted_year_built"] = ":".join(cell_text.split(":")[1:]).strip()
            elif "Year Built:" in cell_text:
                property_dict["year_built"] = ":".join(cell_text.split(":")[1:]).strip()
        except (AttributeError, IndexError):
            continue

    # Define data from tables
    data_tables = history_property_page.find_all("table")
    for data_table in data_tables:
        try:
            table_header = data_table.find("tr", class_="tableheaders").text
            if "Owner Name(s)" in table_header:
                property_dict["owners"] = parse_one_column_table(data_table)
            elif "Assessor Parcel Maps Associated" in table_header:
                property_dict["Assessor Parcel Maps Associated with Schedule"] = parse_one_column_table(data_table)
            elif "Land Characteristics" in table_header:
                property_dict["land_characteristics"] = parse_one_column_table(data_table)
            elif (
                "Block" in table_header and
                "Lot" in table_header and
                "Key" in table_header
                ):
                property_dict["property_description"] =  parse_many_columns_table(data_table, name="property_description")
            elif (
                "Item" in table_header and
                "Quality" in table_header
                ):
                property_dict["property_inventory_1"] =  parse_many_columns_table(data_table)
            elif (
                "Areas" in table_header and
                "Quality" in table_header
                ):
                property_dict["property_inventory_2"] =  parse_many_columns_table(data_table)
            elif (
                "Adjustment Code" in table_header and
                "Adjustment SqFt" in table_header
                ):
                property_dict["property_inventory_3"] =  parse_many_columns_table(data_table)
            elif (
                "Sale Date" in table_header and
                "Sale Amount" in table_header
                ):
                property_dict["sales_history"] =  parse_many_columns_table(data_table)
            elif (
                "Payable" in table_header and not data_table.table
                ):
                property_dict["tax_information"] =  parse_many_columns_table(data_table, name="tax_info")
            elif (
                "Mill Levy" in table_header and not data_table.table
                ):
                property_dict["mill_levy_information"] =  parse_many_columns_table(data_table, name="mill_levy_information")
        except AttributeError:
            pass

        if "Property Address:" in data_table.text and not data_table.table:
            address_data = parse_address_table(data_table)
            property_dict["property_address"] = address_data[0]
            property_dict["mailing_address"] = address_data[1]
    print(property_dict)
    return property_dict


def parse_one_column_table(data_table):
    """Parse tables with only one column"""
    output_list = []
    data_rows = data_table.find_all("tr")[1:]
    for data_row in data_rows:
        data_cells = data_row.find_all("td")
        for data_cell in data_cells:
            try:
                output_list.append(data_cell.text.strip())
            except AttributeError:
                continue
    return ", ".join(output_list)


def parse_many_columns_table(data_table, name=""):
    """Parse tables with more that one columns"""
    raw_table_rows = data_table.find_all("tr")
    table_data_list = []
    if name == "property_description":
        data_rows = raw_table_rows[1:-1]
    elif name == "tax_info":
        data_dict = {}
        data_rows = raw_table_rows[1:]
        for i, data_row in enumerate(data_rows):
            if (
                i % 2 != 0 or
                i == len(data_rows)
                ):
                continue
            else:
                field_cells = data_row.find_all("td")
                field_name = field_cells[1].text.strip().lower().replace(" ", "_")
                value_cells = data_rows[i + 1].find_all("td")
                value_name = value_cells[1].text.strip()
                data_dict[field_name] = value_name
        return data_dict
    elif name == "mill_levy_information":
        data_dict = {}
        data_rows = raw_table_rows[1:]
        for data_row in data_rows:
            cells = data_row.find_all("td")
            field_name = cells[0].text.strip().lower().replace(" ", "_")
            value_name = cells[1].text.strip()
            data_dict[field_name] = value_name
        return data_dict
    else:
        data_rows = raw_table_rows[1:]

    header_cells = raw_table_rows[0].find_all("td")
    headers = [header_tag.text.strip().lower() for header_tag in header_cells]
    for i, data_row in enumerate(data_rows):
        row_dict = {}
        data_cells = data_row.find_all("td")
        for i, data_cell in enumerate(data_cells):
            row_dict[headers[i].replace(" ", "_")] = data_cells[i].text.strip()
        table_data_list.append(row_dict)
    return table_data_list


def parse_address_table(data_table):
    """Parse address data"""
    data_rows = data_table.find_all("tr")
    property_address_tokens = []
    mailing_address_tokens = []
    row_header = ""
    for data_row in data_rows:
        try:
            data_cells = data_row.find_all("td")
            field_name = data_cells[0].text.strip()
            field_value = data_cells[1].text.strip()
            if "Property Address:" in field_name:
                property_address_tokens.append(field_value)
                row_header = "Property Address"
            elif "Mailing Address:" in field_name:
                mailing_address_tokens.append(field_value)
                row_header = "Mailing Address"
            elif not field_name and row_header == "Property Address":
                property_address_tokens.append(field_value)
            elif not field_name and row_header == "Mailing Address":
                mailing_address_tokens.append(field_value)
        except (AttributeError, IndexError):
            continue

    property_address = " ".join(" ".join(property_address_tokens).split())
    mailing_address = " ".join(" ".join(mailing_address_tokens).split())
    return property_address, mailing_address
