import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

print("=" * 60)
print("📊 СТАТИСТИКА: p-value и доверительные интервалы")
print("=" * 60)

# --------------------------------------------------------------
# 1. Генерируем две группы случайных данных
# --------------------------------------------------------------
np.random.seed(42)

# Группа А (контроль) — продажи до изменений
group_a = np.random.normal(loc=5000, scale=500, size=100)  # среднее 5000, разброс 500

# Группа Б (тест) — продажи после изменений (сдвиг на 200 руб)
group_b = np.random.normal(loc=5200, scale=500, size=100)  # среднее 5200

print(f"Группа А (контроль): среднее = {group_a.mean():.0f}, std = {group_a.std():.0f}")
print(f"Группа Б (тест):    среднее = {group_b.mean():.0f}, std = {group_b.std():.0f}")
print(f"Разница: {group_b.mean() - group_a.mean():.0f} руб.")

# --------------------------------------------------------------
# 2. t-test (сравнение двух групп)
# --------------------------------------------------------------
t_stat, p_value = stats.ttest_ind(group_a, group_b)

print(f"\n📈 РЕЗУЛЬТАТ t-test:")
print(f"   t-statistic: {t_stat:.4f}")
print(f"   p-value: {p_value:.4f}")

if p_value < 0.05:
    print("   ✅ Вывод: Разница статистически значима (p < 0.05)")
    print("   → Изменения действительно повлияли на продажи")
else:
    print("   ❌ Вывод: Разница не значима (p > 0.05)")
    print("   → Изменения не дали эффекта")

# --------------------------------------------------------------
# 3. Доверительный интервал
# --------------------------------------------------------------
confidence_level = 0.95
degrees_freedom = len(group_a) + len(group_b) - 2
mean_diff = group_b.mean() - group_a.mean()
std_err = np.sqrt(group_a.var() / len(group_a) + group_b.var() / len(group_b))

# Критическое значение t
t_critical = stats.t.ppf((1 + confidence_level) / 2, degrees_freedom)

margin_error = t_critical * std_err
ci_lower = mean_diff - margin_error
ci_upper = mean_diff + margin_error

print(f"\n📊 ДОВЕРИТЕЛЬНЫЙ ИНТЕРВАЛ (95%):")
print(f"   Разница средних: {mean_diff:.0f} руб.")
print(f"   Интервал: [{ci_lower:.0f}, {ci_upper:.0f}] руб.")

if ci_lower > 0:
    print("   ✅ Весь интервал выше 0 → изменения точно увеличили продажи")
elif ci_upper < 0:
    print("   ❌ Весь интервал ниже 0 → изменения уменьшили продажи")
else:
    print("   ⚠️ Интервал пересекает 0 → эффект не доказан")

# --------------------------------------------------------------
# 4. Визуализация
# --------------------------------------------------------------
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.hist(group_a, alpha=0.5, label='Группа А (контроль)', bins=15)
plt.hist(group_b, alpha=0.5, label='Группа Б (тест)', bins=15)
plt.axvline(group_a.mean(), color='blue', linestyle='dashed', linewidth=2)
plt.axvline(group_b.mean(), color='orange', linestyle='dashed', linewidth=2)
plt.xlabel('Сумма продаж (руб.)')
plt.ylabel('Частота')
plt.title('Распределение продаж')
plt.legend()

plt.subplot(1, 2, 2)
plt.errorbar(x=['Группа А', 'Группа Б'],
             y=[group_a.mean(), group_b.mean()],
             yerr=[group_a.std(), group_b.std()],
             fmt='o', capsize=10, markersize=10)
plt.ylabel('Средняя сумма (руб.)')
plt.title('Средние с доверительными интервалами')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('statistics_intro.png', dpi=100)
plt.close()

print(f"\n📊 График сохранен: statistics_intro.png")