import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

print("=" * 60)
print("📊 CHI-SQUARE TEST: Влияние пола на покупку")
print("=" * 60)

# --------------------------------------------------------------
# 1. Создаем данные
# --------------------------------------------------------------
np.random.seed(42)

# Мужчины: 500 человек, 120 купили (24%)
n_men = 500
bought_men = 120
not_bought_men = n_men - bought_men

# Женщины: 500 человек, 160 купили (32%)
n_women = 500
bought_women = 130
not_bought_women = n_women - bought_women

# Таблица сопряженности (contingency table)
#               Купили   Не купили
# Мужчины       bought   not_bought
# Женщины       bought   not_bought

table = [
    [bought_men, not_bought_men],
    [bought_women, not_bought_women]
]

print("\n📁 Таблица сопряженности (купили / не купили):")
print(pd.DataFrame(table, index=['Мужчины', 'Женщины'], columns=['Купили', 'Не купили']))

# --------------------------------------------------------------
# 2. Chi-square тест
# --------------------------------------------------------------
chi2, p_value, dof, expected = chi2_contingency(table)

print(f"\n📈 РЕЗУЛЬТАТЫ CHI-SQUARE ТЕСТА:")
print(f"   Chi-square: {chi2:.4f}")
print(f"   p-value: {p_value:.4f}")
print(f"   Степени свободы: {dof}")

print(f"\n📊 Ожидаемые значения (если бы пол не влиял):")
expected_df = pd.DataFrame(expected, index=['Мужчины', 'Женщины'], columns=['Купили', 'Не купили'])
print(expected_df)

if p_value < 0.05:
    print("\n   ✅ Вывод: Разница статистически значима (p < 0.05)")
    print("   → Пол влияет на вероятность покупки")
else:
    print("\n   ❌ Вывод: Разница не значима (p > 0.05)")
    print("   → Пол не влияет на покупку")

# --------------------------------------------------------------
# 3. Визуализация
# --------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# График 1: Столбцы
axes[0].bar(['Мужчины', 'Женщины'], [bought_men/n_men*100, bought_women/n_women*100],
            color=['blue', 'pink'], edgecolor='black')
axes[0].set_ylabel('Конверсия (%)')
axes[0].set_title('Конверсия по полу')
axes[0].set_ylim(0, max(bought_men/n_men*100, bought_women/n_women*100) * 1.2)
for i, val in enumerate([bought_men/n_men*100, bought_women/n_women*100]):
    axes[0].text(i, val + 0.5, f'{val:.1f}%', ha='center')

# График 2: Stacked bar (количество)
x = ['Мужчины', 'Женщины']
not_bought = [not_bought_men, not_bought_women]
bought = [bought_men, bought_women]

axes[1].bar(x, not_bought, label='Не купили', color='lightcoral')
axes[1].bar(x, bought, bottom=not_bought, label='Купили', color='lightgreen')
axes[1].set_ylabel('Количество человек')
axes[1].set_title('Распределение покупок по полу')
axes[1].legend()

plt.tight_layout()
plt.savefig('chi_square_test.png', dpi=100)
plt.close()

print(f"\n📊 График сохранен: chi_square_test.png")

# --------------------------------------------------------------
# 4. Вывод для бизнеса
# --------------------------------------------------------------
print("\n" + "=" * 60)
print("💼 ВЫВОД ДЛЯ БИЗНЕСА")
print("=" * 60)

diff = (bought_women/n_women - bought_men/n_men) * 100
print(f"\nЖенщины покупают на {diff:.1f}% чаще мужчин.")
if p_value < 0.05:
    print("✅ Разница статистически значима.")
    print("📌 Рекомендация: таргетировать рекламу на женщин.")
else:
    print("⚠️ Разница не значима.")
    print("📌 Рекомендация: разделение по полу неэффективно.")

print("\n" + "=" * 60)
print("✅ Анализ завершен!")
print("=" * 60)