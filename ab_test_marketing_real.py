import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import os

print("=" * 60)
print("📊 A/B ТЕСТ НА РЕАЛЬНЫХ ДАННЫХ")
print("Маркетинговые кампании (отклик клиентов)")
print("=" * 60)

# --------------------------------------------------------------
# 1. Загружаем данные
# --------------------------------------------------------------
df = pd.read_excel('marketing_campaign_dataset.xlsx')

print(f"\n📁 Данные загружены: {df.shape[0]} строк, {df.shape[1]} колонок")

# --------------------------------------------------------------
# 2. Определяем колонки
# --------------------------------------------------------------
# Ищем колонку с откликом (Response)
response_col = None
for col in df.columns:
    if 'response' in col.lower() or 'accepted' in col.lower():
        response_col = col
        break

if response_col is None:
    print("⚠️ Колонка 'Response' не найдена. Использую первую бинарную колонку")
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64'] and df[col].nunique() <= 2:
            response_col = col
            break

print(f"\n📋 Определены колонки:")
print(f"   Отклик на кампанию: {response_col}")

# --------------------------------------------------------------
# 3. Создаем группы для A/B теста
# --------------------------------------------------------------
# В этом датасете нет явной группы "тест/контроль"
# Мы создадим две группы случайным образом для демонстрации
np.random.seed(42)

# Создаем колонку "group" (50% контроль, 50% тест)
df['group'] = np.random.choice(['control', 'test'], size=len(df), p=[0.5, 0.5])

# Для тестовой группы "включаем" кампанию (имитация)
# В реальности здесь были бы разные условия
df['converted'] = df[response_col]

print(f"\n📊 РАСПРЕДЕЛЕНИЕ ПО ГРУППАМ:")
print(f"   Контрольная группа: {len(df[df['group'] == 'control'])} клиентов")
print(f"   Тестовая группа: {len(df[df['group'] == 'test'])} клиентов")

# --------------------------------------------------------------
# 4. Считаем конверсию по группам
# --------------------------------------------------------------
control_conv = df[df['group'] == 'control']['converted'].mean() * 100
test_conv = df[df['group'] == 'test']['converted'].mean() * 100

print(f"\n📊 КОНВЕРСИЯ (отклик на кампанию):")
print(f"   Контрольная группа: {control_conv:.2f}%")
print(f"   Тестовая группа:    {test_conv:.2f}%")
print(f"   Разница: {test_conv - control_conv:.2f}%")

# --------------------------------------------------------------
# 5. Таблица сопряженности и Chi-square тест
# --------------------------------------------------------------
contingency = pd.crosstab(df['group'], df['converted'])
print(f"\n📁 Таблица сопряженности (откликнулись / не откликнулись):")
print(contingency)

chi2, p_value, dof, expected = chi2_contingency(contingency)

print(f"\n📈 РЕЗУЛЬТАТЫ CHI-SQUARE ТЕСТА:")
print(f"   Chi-square: {chi2:.4f}")
print(f"   p-value: {p_value:.6f}")
print(f"   Степени свободы: {dof}")

if p_value < 0.05:
    print("\n   ✅ Вывод: Разница статистически значима (p < 0.05)")
    print("   → Тестовая группа откликнулась на кампанию значимо лучше")
else:
    print("\n   ❌ Вывод: Разница не значима (p > 0.05)")
    print("   → Тест не показал значимого эффекта")

# --------------------------------------------------------------
# 6. Доверительный интервал
# --------------------------------------------------------------
p_control = control_conv / 100
p_test = test_conv / 100
n_control = len(df[df['group'] == 'control'])
n_test = len(df[df['group'] == 'test'])

se = np.sqrt(p_control*(1-p_control)/n_control + p_test*(1-p_test)/n_test)
z_critical = 1.96
ci_lower = (p_test - p_control) - z_critical * se
ci_upper = (p_test - p_control) + z_critical * se

print(f"\n📊 ДОВЕРИТЕЛЬНЫЙ ИНТЕРВАЛ (95%):")
print(f"   Разница конверсий: {(p_test - p_control)*100:.2f}%")
print(f"   Интервал: [{ci_lower*100:.2f}%, {ci_upper*100:.2f}%]")

# --------------------------------------------------------------
# 7. Визуализация
# --------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# График 1: Конверсия по группам
axes[0].bar(['Контроль', 'Тест'], [control_conv, test_conv],
            color=['#3498db', '#2ecc71'], edgecolor='black')
axes[0].set_ylabel('Отклик (%)')
axes[0].set_title('Отклик на кампанию по группам')
axes[0].set_ylim(0, max(control_conv, test_conv) * 1.2)
for i, val in enumerate([control_conv, test_conv]):
    axes[0].text(i, val + 0.5, f'{val:.1f}%', ha='center')

# График 2: Stacked bar
conv_counts = df.groupby(['group', 'converted']).size().unstack()
conv_counts.columns = ['Не откликнулись', 'Откликнулись']
conv_counts.plot(kind='bar', stacked=True, ax=axes[1], color=['#e74c3c', '#2ecc71'])
axes[1].set_xlabel('Группа')
axes[1].set_ylabel('Количество клиентов')
axes[1].set_title('Распределение откликов')
axes[1].legend()
axes[1].tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.savefig('ab_test_marketing_real.png', dpi=100)
plt.close()

print(f"\n📊 График сохранен: ab_test_marketing_real.png")

# --------------------------------------------------------------
# 8. Бизнес-вывод
# --------------------------------------------------------------
print("\n" + "=" * 60)
print("💼 ФИНАЛЬНЫЙ ВЫВОД ДЛЯ БИЗНЕСА")
print("=" * 60)

if p_value < 0.05:
    print(f"\n✅ Маркетинговая кампания увеличила отклик на {test_conv - control_conv:.2f}%")
    print(f"   (p-value = {p_value:.4f}, 95% CI: [{ci_lower*100:.1f}%, {ci_upper*100:.1f}%])")
    print("\n📌 Рекомендация: Продолжать использовать данную стратегию кампании.")
else:
    print(f"\n❌ Кампания не показала статистически значимого эффекта")
    print(f"   (p-value = {p_value:.4f})")
    print("\n📌 Рекомендация: Пересмотреть стратегию или увеличить выборку.")

print("\n" + "=" * 60)
print("✅ Анализ завершен!")
print("=" * 60)