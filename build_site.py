import glob
import os
import shutil

from jinja2 import Environment, FileSystemLoader
import markdown


to_delete = glob.glob('*.html') + glob.glob('*.css') + glob.glob('*.js')
[os.remove(i) for i in to_delete]

content_files = glob.glob('src/content/*')
actual_content_files = glob.glob('src/content/*.md') + glob.glob('src/content/*/*.md')
env = Environment(
    loader=FileSystemLoader('src/templating/'),
)
template = env.get_template('content.html')
list_template = env.get_template('list.html')

nav_links = {i.replace('.md', '').replace('src/content/', '').replace('index', 'about').title(): i.replace('.md', '').replace('src/content/', '').replace('/', '.') + '.html' for i in content_files}
for page in actual_content_files:
    print(page)
    with open(page, encoding='utf-8') as file:
        content = markdown.markdown(
            file.read(),
        )
    rendered_content = template.render(
        content=content,
        navlinks=nav_links
    )
    with open(f"{page.replace('src/content/', '').replace('md', 'html').replace('/', '.')}", 'w', encoding='utf-8') as file:
        file.write(rendered_content)

for dir in [i for i in content_files if os.path.isdir(i)]:
    print(dir)
    items = glob.glob(f"{dir}/*")
    items = {i.replace('.md', '').replace(f'{dir}/', ''): i.replace('.md', '.html').replace('src/content/', '').replace('/', '.') for i in items}
    rendered_content = list_template.render(
        navlinks=nav_links,
        links=items,
        title=dir.replace('src/content/', ''),
    )
    with open(f"{dir.split('/')[-1]}.html", 'w', encoding='utf-8') as file:
        file.write(rendered_content)



# now just copy over any js / css files
content_files = glob.glob('src/templating/*')
for item in [i for i in content_files if i.endswith('.js') or i.endswith('.css')]:
    print(item)
    shutil.copy(item, item.replace('src/templating/', ''))

# and finally, copy over the .assets folder
shutil.rmtree('.assets')
shutil.copytree('src/content/.assets', '.assets')
