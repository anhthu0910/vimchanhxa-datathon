import json

nb_path = 'd:/datathon/vimchanhxa-datathon/notebooks/03_EDA_DEMO.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'Trend của Revenue và Cogs toàn bộ giai đoạn' in source:
            
            code_lines = [
                '\n',
                '# Sắp xếp dữ liệu theo thời gian để tính rolling mean chính xác\n',
                'df_sales_sorted = df_sales.sort_values(\"date\")\n',
                '\n',
                '# Tính Rolling Mean (Trung bình trượt) với cửa sổ 30 ngày (có thể điều chỉnh)\n',
                'window_size = 30\n',
                'df_sales_sorted[\"revenue_trend\"] = df_sales_sorted[\"revenue\"].rolling(window=window_size).mean()\n',
                'df_sales_sorted[\"cogs_trend\"] = df_sales_sorted[\"cogs\"].rolling(window=window_size).mean()\n',
                '\n',
                '# Vẽ biểu đồ\n',
                'plt.figure(figsize=(16, 8))\n',
                '\n',
                '# Vẽ 2 đường trend trên cùng 1 axes\n',
                'plt.plot(\n',
                '    df_sales_sorted[\"date\"],\n',
                '    df_sales_sorted[\"revenue_trend\"],\n',
                '    color=\"#1f77b4\",\n',
                '    linewidth=2.5,\n',
                '    label=f\"Revenue Trend ({window_size} days rolling mean)\"\n',
                ')\n',
                '\n',
                'plt.plot(\n',
                '    df_sales_sorted[\"date\"],\n',
                '    df_sales_sorted[\"cogs_trend\"],\n',
                '    color=\"#ff7f0e\",\n',
                '    linewidth=2.5,\n',
                '    label=f\"COGS Trend ({window_size} days rolling mean)\"\n',
                ')\n',
                '\n',
                'plt.title(\n',
                '    \"Xu hướng (Trend) của Revenue và COGS toàn bộ giai đoạn\",\n',
                '    fontsize=16,\n',
                '    fontweight=\"bold\",\n',
                '    pad=15\n',
                ')\n',
                '\n',
                'plt.xlabel(\"Thời gian\", fontsize=12)\n',
                'plt.ylabel(\"Giá trị\", fontsize=12)\n',
                '\n',
                '# Format trục X\n',
                'plt.gca().xaxis.set_major_locator(mdates.YearLocator())\n',
                'plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(\"%Y\"))\n',
                'plt.xticks(rotation=45)\n',
                '\n',
                'plt.grid(axis=\"y\", linestyle=\"--\", alpha=0.7)\n',
                'plt.legend(loc=\"upper left\", fontsize=12)\n',
                'plt.tight_layout()\n',
                'plt.show()\n'
            ]
            
            cell['source'] = [cell['source'][0].rstrip('\n') + '\n'] + code_lines
            break

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
