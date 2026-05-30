with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_idx = html.find('<!-- Top Header -->')
end_idx = html.find('<!-- Footer -->')
if end_idx == -1: end_idx = html.find('<footer')

new_content = html[:start_idx] + '''
<!-- Top Header -->
<header class="flex justify-between items-center mb-xl">
<div>
<h2 class="font-headline-lg text-headline-lg">Settings</h2>
<p class="font-body-md text-body-md text-on-surface-variant">Manage your account and preferences.</p>
</div>
</header>
<div class="glass-card p-xl rounded-xl flex flex-col items-center justify-center text-center space-y-md min-h-[50vh]">
<span class="material-symbols-outlined text-[64px] text-primary/50">settings</span>
<h3 class="font-headline-md text-headline-md">Settings Module Inactive</h3>
<p class="font-body-md text-body-md text-on-surface-variant max-w-md">The settings module is currently under construction. Please return later to manage your preferences.</p>
</div>
''' + html[end_idx:]

new_content = new_content.replace('<a class="flex items-center gap-md px-md py-sm rounded-lg bg-primary-container/20 text-primary border-r-4 border-primary transition-all duration-200" data-inroad-nav="dashboard" href="/dashboard.html">', '<a class="flex items-center gap-md px-md py-sm rounded-lg text-on-surface-variant hover:bg-surface-variant/50 hover:translate-x-1 transition-all duration-200" data-inroad-nav="dashboard" href="/dashboard.html">')

new_content = new_content.replace('<a class="flex items-center gap-md px-md py-sm rounded-lg text-on-surface-variant hover:bg-surface-variant/50 hover:translate-x-1 transition-all duration-200" href="#">\n<span class="material-symbols-outlined">settings</span>\n<span class="font-data-sm text-data-sm">Settings</span>\n</a>', '<a class="flex items-center gap-md px-md py-sm rounded-lg bg-primary-container/20 text-primary border-r-4 border-primary transition-all duration-200" href="/settings.html">\n<span class="material-symbols-outlined" style="font-variation-settings: \'FILL\' 1;">settings</span>\n<span class="font-data-sm text-data-sm">Settings</span>\n</a>')

with open('settings.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
