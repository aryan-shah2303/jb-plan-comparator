import os
from flask import Flask, render_template, request

app = Flask(__name__)

jb_plans = [
    {
        "name": "$59 Plan",
        "monthly_cost": 59,
        "duration_months": 24,
        "gift_card": 0,
        "data_gb": 60
    },
    {
        "name": "$79 Plan",
        "monthly_cost": 79,
        "duration_months": 24,
        "gift_card": 550,
        "data_gb": 150
    },
    {
        "name": "$89 Plan",
        "monthly_cost": 89,
        "duration_months": 24,
        "gift_card": 1000,
        "data_gb": 300
    }
]

@app.route('/', methods=['GET', 'POST'])
def index():
    best_plan = None
    results = []

    if request.method == 'POST':
        current_cost = float(request.form['current_cost'])
        current_data = float(request.form['current_data'])
        phone_cost = float(request.form['phone_cost'])

        current_total = current_cost * 24
        current_monthly_total = current_cost
        current_weekly_total = current_cost / 4

        for plan in jb_plans:
            total_plan_cost = plan['monthly_cost'] * plan['duration_months']
            effective_cost = total_plan_cost - plan['gift_card']
            total_cost = effective_cost + phone_cost
            monthly_cost = effective_cost / 24
            weekly_cost = monthly_cost / 4
            weekly_diff = weekly_cost - current_weekly_total
            data_gain = plan['data_gb'] - current_data

            results.append({
                'name': plan['name'],
                'monthly_cost': plan['monthly_cost'],
                'data_gb': plan['data_gb'],
                'gift_card': plan['gift_card'],
                'total_cost': total_cost,
                'effective_plan_cost': effective_cost,
                'monthly_after_gift': round(monthly_cost, 2),
                'weekly_after_gift': round(weekly_cost, 2),
                'weekly_diff': round(weekly_diff, 2),
                'data_gain': data_gain
            })

        best_plan = min(results, key=lambda x: x['total_cost'])

        return render_template('index.html',
                               results=results,
                               current_total=current_total,
                               current_monthly=current_monthly_total,
                               current_weekly=current_weekly_total,
                               best_plan=best_plan)

    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
