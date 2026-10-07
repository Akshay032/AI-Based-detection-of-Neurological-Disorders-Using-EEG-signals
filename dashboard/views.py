from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import Prediction
from app.utils import run_prediction

@login_required
def dashboard_view(request):
    total = Prediction.objects.filter(user=request.user).count()
    return render(request, 'dashboard/dashboard.html', {'total': total})

@login_required
def predict_view1(request):
    if request.method == "POST":
        values = request.POST['data'].split(',')
        result = run_prediction(values)

        Prediction.objects.create(
            user=request.user,
            input_data=str(values),
            result=str(result)
        )

        return render(request, 'predict.html', {'result': result})

    return render(request, 'predict.html')

@login_required
def history_view(request):
    predictions = Prediction.objects.filter(user=request.user)
    return render(request, 'history.html', {'predictions': predictions})
@login_required
def predict_view(request):

    result = None

    if request.method == "POST":

        data = request.POST.get("features")

        # convert comma separated values to list
        values = [float(x.strip()) for x in data.split(",")]

        if len(values) != 178:
            return render(request, 'dashboard/predict.html', {
                'error': "Please enter exactly 178 values."
            })

        result = run_prediction(values)

        Prediction.objects.create(
            user=request.user,
            input_data=str(values),
            result=str(result)
        )

    return render(request, 'dashboard/predict.html', {
        'result': result
    })
@login_required
def history_view(request):
    return render(request, 'dashboard/history.html')
@login_required
def my_predictions(request):
    predictions = Prediction.objects.filter(user=request.user)
    return render(request, 'dashboard/my_predictions.html', {'predictions': predictions})
@login_required
def profile_page(request):
    profile = request.user.profile
    return render(request, 'dashboard/profile.html', {
        'profile': profile
    })
