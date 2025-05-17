from jinja2 import Environment, FileSystemLoader


def generate_report(clusters_data: dict, failures_data: dict, clustered_failures, template_path: str = "./modules/report", template_filename: str = "report.html"):
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template(template_filename)
    
    html_output = template.render(
        total_failures=len(failures_data),
        total_clusters=len(set(clustered_failures)),
        clusters=clusters_data
    )

    with open('./report.html', 'w', encoding='utf-8') as f:
        f.write(html_output)

