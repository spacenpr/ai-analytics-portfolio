import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 60)
print("📊 АНАЛИЗ МАРКЕТИНГОВЫХ КАМПАНИЙ")
print("Сравнение эффективности разных каналов и типов")
print("=" * 60)

# --------------------------------------------------------------
# 1. Загружаем данные
# --------------------------------------------------------------
df = pd.read_excel('marketing_campaign_dataset.xlsx')
print(f"\n📁 Данные загружены: {df.shape[0]:,} строк, {df.shape[1]} колонок")

# --------------------------------------------------------------
# 2. Смотрим, какие есть каналы и типы кампаний
# --------------------------------------------------------------
print(f"\n📋 Каналы (Channel_Used): {df['Channel_Used'].unique()}")
print(f"\n📋 Типы кампаний (Campaign_Type): {df['Campaign_Type'].unique()}")

# --------------------------------------------------------------
# 3. Сравнение Conversion_Rate по каналам
# --------------------------------------------------------------
print("\n" + "=" * 60)
print("📊 СРАВНЕНИЕ CONVERSION_RATE ПО КАНАЛАМ")
print("=" * 60)

channel_stats = df.groupby('Channel_Used')['Conversion_Rate'].agg(['mean', 'std', 'count']).round(2)
print(channel_stats)

# --------------------------------------------------------------
# 4. Визуализация: Conversion_Rate по каналам
# --------------------------------------------------------------
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Channel_Used', y='Conversion_Rate', palette='Set2')
plt.title('Распределение Conversion Rate по каналам', fontsize=14)
plt.xlabel('Канал')
plt.ylabel('Conversion Rate (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('conversion_by_channel.png', dpi=100)
plt.close()
print(f"\n📊 График сохранен: conversion_by_channel.png")

# --------------------------------------------------------------
# 5. Статистический тест: Email vs Social Media
# --------------------------------------------------------------
print("\n" + "=" * 60)
print("📈 СТАТИСТИЧЕСКИЙ ТЕСТ: Email vs Social Media")
print("=" * 60)

email_conv = df[df['Channel_Used'] == 'Email']['Conversion_Rate']
social_conv = df[df['Channel_Used'] == 'Social Media']['Conversion_Rate']

t_stat, p_value = ttest_ind(email_conv, social_conv)

print(f"Email: средняя конверсия = {email_conv.mean():.2f}%")
print(f"Social Media: средняя конверсия = {social_conv.mean():.2f}%")
print(f"Разница: {social_conv.mean() - email_conv.mean():.2f}%")
print(f"\n📈 t-test результат:")
print(f"   t-statistic: {t_stat:.4f}")
print(f"   p-value: {p_value:.6f}")

if p_value < 0.05:
    print("   ✅ Разница статистически значима (p < 0.05)")
    print("   → Social Media эффективнее Email")
else:
    print("   ❌ Разница не значима (p > 0.05)")

# --------------------------------------------------------------
# 6. Сравнение ROI по типам кампаний
# --------------------------------------------------------------
print("\n" + "=" * 60)
print("💰 СРАВНЕНИЕ ROI ПО ТИПАМ КАМПАНИЙ")
print("=" * 60)

campaign_type_stats = df.groupby('Campaign_Type')['ROI'].agg(['mean', 'std', 'count']).round(2)
print(campaign_type_stats)

# --------------------------------------------------------------
# 7. Визуализация: ROI по типам кампаний
# --------------------------------------------------------------
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Campaign_Type', y='ROI', palette='viridis', errorbar='ci')
plt.title('Средний ROI по типам кампаний (95% доверительный интервал)', fontsize=14)
plt.xlabel('Тип кампании')
plt.ylabel('ROI (%)')
plt.tight_layout()
plt.savefig('roi_by_campaign_type.png', dpi=100)
plt.close()
print(f"\n📊 График сохранен: roi_by_campaign_type.png")

# --------------------------------------------------------------
# 8. Корреляция между метриками
# --------------------------------------------------------------
print("\n" + "=" * 60)
print("🔍 КОРРЕЛЯЦИЯ МЕЖДУ МЕТРИКАМИ")
print("=" * 60)

corr_cols = ['Conversion_Rate', 'Acquisition_Cost', 'ROI', 'Clicks', 'Impressions', 'Engagement_Score']
corr_matrix = df[corr_cols].corr()
print("\nКорреляционная матрица:")
print(corr_matrix.round(3))

# Тепловая карта корреляции
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Корреляция между метриками', fontsize=14)
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=100)
plt.close()
print(f"\n📊 График сохранен: correlation_heatmap.png")

# --------------------------------------------------------------
# 9. Самые эффективные кампании
# --------------------------------------------------------------
print("\n" + "=" * 60)
print("🏆 ТОП-10 САМЫХ ЭФФЕКТИВНЫХ КАМПАНИЙ")
print("=" * 60)

top_campaigns = df.nlargest(10, 'ROI')[['Campaign_ID', 'Company', 'Campaign_Type', 'Channel_Used', 'ROI', 'Conversion_Rate']]
print(top_campaigns.to_string(index=False))

# --------------------------------------------------------------
# 10. Финальный вывод
# --------------------------------------------------------------
print("\n" + "=" * 60)
print("💼 ФИНАЛЬНЫЙ ВЫВОД ДЛЯ БИЗНЕСА")
print("=" * 60)

best_channel = channel_stats['mean'].idxmax()
best_channel_value = channel_stats['mean'].max()
best_type = campaign_type_stats['mean'].idxmax()
best_type_value = campaign_type_stats['mean'].max()

print(f"""
📌 РЕКОМЕНДАЦИИ:

1. Лучший канал: {best_channel} (средняя конверсия {best_channel_value:.1f}%)
   → Рекомендуется увеличить бюджет на этот канал

2. Лучший тип кампании: {best_type} (средний ROI {best_type_value:.1f}%)
   → Этот тип показывает максимальную окупаемость

3. Корреляционный анализ:
   { 'ROI сильно коррелирует с Conversion_Rate' if abs(corr_matrix.loc['ROI', 'Conversion_Rate']) > 0.5 else 'ROI слабо зависит от Conversion_Rate' }

4. Для дальнейшего анализа:
   • Провести A/B тест между {best_channel} и худшим каналом
   • Исследовать сезонность (если есть данные по датам)
   • Проанализировать Engagement Score в разрезе кампаний
""")

print("\n" + "=" * 60)
print("✅ Анализ завершен!")
print("=" * 60)