import csv
import json

def convert_to_csv(json_filename, csv_filename):
    with open(json_filename, 'r', encoding='utf-8') as jsonfile:
        products_data = json.load(jsonfile)

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            "Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Product Type",
            "Tags", "Option1 Name", "Option1 Value", "Variant SKU", "Variant Price",
            "Image Src", "Published", "Variant Inventory Tracker", "Variant Inventory Qty",
            "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Requires Shipping",
            "Variant Taxable", "SEO Title", "SEO Description", "Status", "Collection",
            "Image Position"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for product_name, product_info in products_data.items():
            handle = product_name.lower().replace(" ", "-")

            description_html = ''
            if product_info['description_images']:
                description_html = '<img src="' + '" /><img src="'.join(product_info['description_images']) + '" />'
            else:
                description_html = product_info['description_text']


            # First write the main line with the primary image
            for size in product_info['sizes']:
                primary_image = "https:" + product_info['imagens'][0] if product_info['imagens'] else ""
                writer.writerow({
                    "Handle": handle,
                    "Title": product_info["title"],
                    "Body (HTML)": description_html,
                    "Vendor": "SpaceSports",
                    "Product Category": "Vestuário e acessórios",
                    "Product Type": "Camisas",
                    "Tags": "Futebol, Camisas, " + product_name,
                    "Option1 Name": "Size",
                    "Option1 Value": size,
                    "Variant SKU": f"{handle}-{size}",
                    "Variant Price": product_info["price"],
                    "Image Src": primary_image,
                    "Published": "TRUE",
                    "Variant Inventory Tracker": "shopify",
                    "Variant Inventory Qty": "100",
                    "Variant Inventory Policy": "deny",
                    "Variant Fulfillment Service": "manual",
                    "Variant Requires Shipping": "TRUE",
                    "Variant Taxable": "TRUE",
                    "SEO Title": product_info["title"],
                    "SEO Description": "Get the latest 2024/25 season jersey now!",
                    "Status": "active",
                    "Collection": "NBA'",
                    "Image Position": 1
                })

                # Now write additional image lines
                for i, img_url in enumerate(product_info['imagens'][1:], start=2):
                    writer.writerow({
                        "Handle": handle,
                        "Image Src": "https:" + img_url,
                        "Image Position": i
                    })

convert_to_csv('product_details.json', 'products.csv')
