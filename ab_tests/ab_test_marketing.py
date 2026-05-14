import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.proportion import proportions_ztest

print("=" * 60)
print("📊 A/B ТЕСТ: Маркетинговая кампания")
print("=" * 60)

# --------------------------------------------------------------
# 1. Создаем синтетические данные (если нет реального файла)
# --------------------------------------------------------------
np.random.seed(42)

# Группа А (контроль) — без рекламы
n_A = 1000
conversions_A = np.random.binomial(1, 0.10, n_A)  # 10% конверсия

# Группа Б (тест) — с рекламой (увеличение на 3%)
n_B = 1000
conversions_B = np.random.binomial(1, 0.13, n_B)  # 13% конверсия

# Собираем DataFrame
df = pd.DataFrame({
    'group': ['A'] * n_A + ['B'] * n_B,
    'converted': list(conversions_A) + list(conversions_B)
})

print(f"\n📁 Данные:")
print(f"   Группа А (контроль): {n_A} пользователей, конверсия = {conversions_A.mean()*100:.1f}%")
print(f"   Группа Б (тест):    {n_B} пользователей, конверсия = {conversions_B.mean()*100:.1f}%")
print(f"   Разница: {conversions_B.mean()*100 - conversions_A.mean()*100:.1f}%")

# --------------------------------------------------------------
# 2. Визуализация
# --------------------------------------------------------------
plt.figure(figsize=(12, 5))

# График 1: Столбцы конверсии
plt.subplot(1, 2, 1)
conversion_rates = df.groupby('group')['converted'].mean() * 100
plt.bar(conversion_rates.index, conversion_rates.values, color=['blue', 'green'])
plt.ylabel('Конверсия (%)')
plt.title('Конверсия по группам')
plt.ylim(0, max(conversion_rates) * 1.2)

for i, rate in enumerate(conversion_rates.values):
    plt.text(i, rate + 0.5, f'{rate:.1f}%', ha='center')

# График 2: Распределение (сколько конверсий в каждой группе)
plt.subplot(1, 2, 2)
conversion_counts = df.groupby(['group', 'converted']).size().unstack()
conversion_counts.plot(kind='bar', stacked=True, ax=plt.gca(), color=['lightcoral', 'lightgreen'])
plt.xlabel('Группа')
plt.ylabel('Количество пользователей')
plt.title('Конверсии и не-конверсии')
plt.legend(['Не купили', 'Купили'])

plt.tight_layout()
plt.savefig('ab_test_marketing.png', dpi=100)
plt.close()
print(f"\n📊 График сохранен: ab_test_marketing.png")

# --------------------------------------------------------------
# 3. Проверка гипотезы (пропорциональный z-test)
# --------------------------------------------------------------
print("\n" + "=" * 60)
print("🔬 СТАТИСТИЧЕСКАЯ ПРОВЕРКА")
print("=" * 60)

# Количество конверсий и размеры групп
successes = [conversions_A.sum(), conversions_B.sum()]
nobs = [n_A, n_B]

# Z-test для пропорций
z_stat, p_value = proportions_ztest(successes, nobs)

print(f"\n📈 Результаты z-test:")
print(f"   z-statistic: {z_stat:.4f}")
print(f"   p-value: {p_value:.4f}")

if p_value < 0.05:
    print("   ✅ Вывод: Разница статистически значима (p < 0.05)")
    print("   → Рекламная кампания ДЕЙСТВИТЕЛЬНО повысила конверсию")
else:
    print("   ❌ Вывод: Разница не значима (p > 0.05)")
    print("   → Рекламная кампания НЕ дала эффекта")

# --------------------------------------------------------------
# 4. Доверительный интервал для разницы конверсий
# --------------------------------------------------------------
p1 = conversions_A.mean()
p2 = conversions_B.mean()
se = np.sqrt(p1*(1-p1)/n_A + p2*(1-p2)/n_B)

# 95% доверительный интервал
z_critical = 1.96
ci_lower = (p2 - p1) - z_critical * se
ci_upper = (p2 - p1) + z_critical * se

print(f"\n📊 ДОВЕРИТЕЛЬНЫЙ ИНТЕРВАЛ (95%):")
print(f"   Разница конверсий: {(p2 - p1)*100:.2f}%")
print(f"   Интервал: [{ci_lower*100:.2f}%, {ci_upper*100:.2f}%]")

if ci_lower > 0:
    print("   ✅ Весь интервал выше 0 → кампания точно увеличила конверсию")
elif ci_upper < 0:
    print("   ❌ Весь интервал ниже 0 → кампания уменьшила конверсию")
else:
    print("   ⚠️ Интервал пересекает 0 → эффект не доказан")

# --------------------------------------------------------------
# 5. Дополнительно: расчет необходимого размера выборки
# --------------------------------------------------------------
print("\n" + "=" * 60)
print("📏 РАЗМЕР ВЫБОРКИ")
print("=" * 60)

from statsmodels.stats.power import zt_ind_solve_power

effect_size = (p2 - p1) / np.sqrt(p1*(1-p1))  # Cohen's h
required_n = zt_ind_solve_power(
    effect_size=effect_size,
    alpha=0.05,
    power=0.8,
    ratio=1.0,
    alternative='two-sided'
)

print(f"\n   Минимальный размер выборки для обнаружения эффекта: {required_n:.0f} на группу")
print(f"   Текущий размер: {n_A} на группу")

if required_n <= n_A:
    print("   ✅ Размер выборки достаточен")
else:
    print(f"   ⚠️ Нужно увеличить выборку до {required_n:.0f}")

print("\n" + "=" * 60)
print("✅ Анализ завершен!")
print("=" * 60)