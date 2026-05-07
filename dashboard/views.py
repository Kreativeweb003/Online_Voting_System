from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# -----------------------
# VOTER DASHBOARD
# -----------------------
@login_required
def voter_dashboard(request):
    user = request.user

    if user.role != "voter":
        return render(request, "403.html")

    return render(request, "dashboard/voter_dashboard.html")


# -----------------------
# CANDIDATE DASHBOARD
# -----------------------
@login_required
def candidate_dashboard(request):
    user = request.user

    if user.role != "candidate":
        return render(request, "403.html")

    return render(request, "dashboard/candidate_dashboard.html")


# -----------------------
# ADMIN DASHBOARD (CUSTOM)
# -----------------------
@login_required
def admin_dashboard(request):
    user = request.user

    if not user.is_superuser:
        return render(request, "403.html")

    return render(request, "dashboard/admin_dashboard.html")