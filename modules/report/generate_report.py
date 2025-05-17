from jinja2 import Environment, FileSystemLoader


def generate_report(clusters_data: dict, failures_data: dict, clustered_failures: dict, template_path: str = "./templates", template_filename: str = "report.html"):
    html_output = template.render(
        total_failures=len(failures_data),
        total_clusters=len(clusters_data_for_template),
        clusters=clusters_data
    )

    with open('./report.html', 'w', encoding='utf-8') as f:
        f.write(html_output)

generate_report({}, {})
