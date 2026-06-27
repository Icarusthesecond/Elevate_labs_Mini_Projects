from flask import Flask, render_template, request, send_from_directory
from scanner import run_scan
from report import generate_pdf

app = Flask(__name__)

scan_history = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        url = request.form["url"]

        results, summary = run_scan(url)

        pdf_file = generate_pdf(results, summary)

        scan_history.append({
            "url": url,
            "vulns": summary['total_vulns'],
            "time": summary['scan_time'],
            "pdf": pdf_file
        })

        return render_template(
            "results.html",
            results=results,
            summary=summary,
            url=url,
            pdf_file=pdf_file,
            success=True,
            history=scan_history
        )

    return render_template("index.html")


@app.route("/download_report/<filename>")
def download_report(filename):
    return send_from_directory("static", filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
