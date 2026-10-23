from datetime import datetime, timezone
from flask import Flask, flash, redirect, render_template, request, url_for
from monitor import check_service
from storage import init_db, add_service, get_services, get_history, delete_service

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-for-production"
init_db()


@app.template_filter("localtime")
def localtime(value):
    if not value:
        return "Never"
    try:
        return datetime.fromisoformat(value).astimezone().strftime("%d %b %Y, %H:%M:%S")
    except (ValueError, TypeError):
        return value


@app.get("/")
def dashboard():
    services = get_services()
    history = get_history(limit=10)
    healthy = sum(1 for s in services if s["last_status"] == "UP")
    down = sum(1 for s in services if s["last_status"] == "DOWN")
    unknown = len(services) - healthy - down
    return render_template(
        "dashboard.html",
        services=services,
        history=history,
        healthy=healthy,
        down=down,
        unknown=unknown,
    )


@app.post("/services")
def create_service():
    name = request.form.get("name", "").strip()
    url = request.form.get("url", "").strip()
    if not name or not url:
        flash("Both service name and URL are required.", "error")
        return redirect(url_for("dashboard"))
    if not url.startswith(("http://", "https://")):
        flash("URL must begin with http:// or https://", "error")
        return redirect(url_for("dashboard"))
    try:
        add_service(name, url)
        flash(f"Added {name}. Run a check to get its first status.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    return redirect(url_for("dashboard"))


@app.post("/services/<int:service_id>/check")
def run_check(service_id):
    services = {s["id"]: s for s in get_services()}
    service = services.get(service_id)
    if not service:
        flash("Service not found.", "error")
        return redirect(url_for("dashboard"))
    result = check_service(service["url"])
    from storage import save_check
    save_check(service_id, result)
    if result["status"] == "UP":
        flash(f'{service["name"]} is UP ({result["response_ms"]:.0f} ms).', "success")
    else:
        flash(f'{service["name"]} is DOWN: {result["message"]}', "error")
    return redirect(url_for("dashboard"))


@app.post("/services/<int:service_id>/delete")
def remove_service(service_id):
    delete_service(service_id)
    flash("Service removed.", "success")
    return redirect(url_for("dashboard"))


@app.get("/health")
def health():
    return {"status": "ok", "application": "DevOps Health Monitor"}, 200


if __name__ == "__main__":
    app.run(debug=True)
