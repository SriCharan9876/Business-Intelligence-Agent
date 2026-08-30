# ============================================
# DATASET SCHEMA
# Skylark Drones BI Agent
#
# This file documents the expected business
# schema for the two monday.com boards.
#
# monday.com data is fetched dynamically.
# This schema is NOT the actual data.
# ============================================


DEALS_SCHEMA = {

    "dataset_name": "Deal Funnel",

    "description": (
        "Sales pipeline data representing "
        "potential and active business "
        "opportunities."
    ),

    "columns": {

        "Deal Name": {
            "type": "text",
            "description":
                "Name or masked identifier of the sales opportunity."
        },

        "Owner code": {
            "type": "text",
            "description":
                "Sales or business development owner responsible for the deal."
        },

        "Client Code": {
            "type": "text",
            "description":
                "Masked customer or client identifier."
        },

        "Deal Status": {
            "type": "category",
            "description":
                "Current status of the opportunity, such as Open, Won, On Hold, or Dead."
        },

        "Close Date (A)": {
            "type": "date",
            "description":
                "Actual date when the deal was closed."
        },

        "Closure Probability": {
            "type": "category",
            "description":
                "Estimated probability of winning the opportunity."
        },

        "Masked Deal value": {
            "type": "numeric",
            "description":
                "Potential monetary value of the sales opportunity."
        },

        "Tentative Close Date": {
            "type": "date",
            "description":
                "Expected or tentative date when the deal may close."
        },

        "Deal Stage": {
            "type": "category",
            "description":
                "Current stage of the sales funnel."
        },

        "Product deal": {
            "type": "text",
            "description":
                "Product or service combination included in the opportunity."
        },

        "Sector/service": {
            "type": "category",
            "description":
                "Industry sector or service category of the opportunity."
        },

        "Created Date": {
            "type": "date",
            "description":
                "Date when the sales opportunity was created."
        }
    }
}


WORK_ORDERS_SCHEMA = {

    "dataset_name": "Work Order Tracker",

    "description": (
        "Operational and financial data for "
        "projects after business has been secured."
    ),

    "columns": {

        "Deal name masked": {
            "type": "text",
            "description":
                "Masked name or identifier of the deal."
        },

        "Customer Name Code": {
            "type": "text",
            "description":
                "Masked customer identifier."
        },

        "Serial #": {
            "type": "text",
            "description":
                "Unique work order or deal reference."
        },

        "Nature of Work": {
            "type": "category",
            "description":
                "Commercial nature of the project, such as one-time, monthly, annual, or proof of concept."
        },

        "Execution Status": {
            "type": "category",
            "description":
                "Current operational execution status of the project."
        },

        "Data Delivery Date": {
            "type": "date",
            "description":
                "Date when project data or deliverables were delivered."
        },

        "Date of PO/LOI": {
            "type": "date",
            "description":
                "Date of the Purchase Order or Letter of Intent."
        },

        "Probable Start Date": {
            "type": "date",
            "description":
                "Expected project start date."
        },

        "Probable End Date": {
            "type": "date",
            "description":
                "Expected project completion date."
        },

        "BD/KAM Personnel code": {
            "type": "text",
            "description":
                "Business Development or Key Account Manager responsible for the work order."
        },

        "Sector": {
            "type": "category",
            "description":
                "Industry sector of the customer or project."
        },

        "Type of Work": {
            "type": "category",
            "description":
                "Type of operational or drone service being delivered."
        },

        "Amount in Rupees (Excl of GST) (Masked)": {
            "type": "numeric",
            "description":
                "Total work order value excluding GST."
        },

        "Amount in Rupees (Incl of GST) (Masked)": {
            "type": "numeric",
            "description":
                "Total work order value including GST."
        },

        "Billed Value in Rupees (Excl of GST.) (Masked)": {
            "type": "numeric",
            "description":
                "Amount already invoiced excluding GST."
        },

        "Billed Value in Rupees (Incl of GST) (Masked)": {
            "type": "numeric",
            "description":
                "Amount already invoiced including GST."
        },

        "Collected Amount in Rupees (Incl. of GST) (Masked)": {
            "type": "numeric",
            "description":
                "Amount of money actually collected from the customer."
        },

        "Amount to be billed in Rs. (Exl. of GST) (Masked)": {
            "type": "numeric",
            "description":
                "Remaining amount to be invoiced excluding GST."
        },

        "Amount to be billed in Rs. (Incl. of GST) (Masked)": {
            "type": "numeric",
            "description":
                "Remaining amount to be invoiced including GST."
        },

        "Amount Receivable (Masked)": {
            "type": "numeric",
            "description":
                "Amount invoiced but not yet collected."
        },

        "Quantity by Ops": {
            "type": "numeric",
            "description":
                "Quantity completed or reported by operations."
        },

        "Quantities as per PO": {
            "type": "numeric",
            "description":
                "Quantity committed in the Purchase Order."
        },

        "Quantity billed (till date)": {
            "type": "numeric",
            "description":
                "Quantity invoiced up to the current date."
        },

        "Balance in quantity": {
            "type": "numeric",
            "description":
                "Remaining quantity to be completed or billed."
        },

        "Invoice Status": {
            "type": "category",
            "description":
                "Current status of invoicing for the work order."
        },

        "Collection status": {
            "type": "category",
            "description":
                "Current payment collection status."
        },

        "Billing Status": {
            "type": "category",
            "description":
                "Overall billing progress status."
        }
    }
}


DATASET_SCHEMA = {

    "deals": DEALS_SCHEMA,

    "work_orders": WORK_ORDERS_SCHEMA
}