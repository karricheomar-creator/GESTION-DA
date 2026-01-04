from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Connexion PostgreSQL
conn = psycopg2.connect(
    dbname="GESTION-DA",
    user="postgres",       # ton utilisateur
    password="omar", # ton mot de passe
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Page d'accueil
@app.route("/")
def index():
    return render_template("index.html")

# Afficher demande en cours
@app.route("/demande")
def demande():
    cur.execute("SELECT * FROM demande_en_cours")
    rows = cur.fetchall()
    return render_template("demande.html", rows=rows)

# Ajouter une demande
@app.route("/add_demande", methods=["POST"])
def add_demande():
    date = request.form["date"]
    affectation = request.form["affectation"]
    type_achat = request.form["type_achat"]
    reference = request.form["reference"]
    quantite = request.form["quantite"]
    observation = request.form["observation"]
    demande_recu = "demande_recu" in request.form

    cur.execute("""
        INSERT INTO demande_en_cours (date, affectation, type_achat, reference, quantite, observation, demande_recu)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (date, affectation, type_achat, reference, quantite, observation, demande_recu))
    conn.commit()
    return redirect("/demande")

# Modifier une demande
@app.route("/edit_demande/<int:n_da>", methods=["GET", "POST"])
def edit_demande(n_da):
    if request.method == "GET":
        cur.execute("SELECT * FROM demande_en_cours WHERE n_da = %s", (n_da,))
        row = cur.fetchone()
        return render_template("edit_demande.html", row=row)
    else:
        date = request.form["date"]
        affectation = request.form["affectation"]
        type_achat = request.form["type_achat"]
        reference = request.form["reference"]
        quantite = request.form["quantite"]
        observation = request.form["observation"]
        demande_recu = "demande_recu" in request.form

        cur.execute("""
            UPDATE demande_en_cours
            SET date=%s, affectation=%s, type_achat=%s, reference=%s, quantite=%s, observation=%s, demande_recu=%s
            WHERE n_da=%s
        """, (date, affectation, type_achat, reference, quantite, observation, demande_recu, n_da))
        conn.commit()
        return redirect("/demande")

# Supprimer une demande
@app.route("/delete_demande/<int:n_da>")
def delete_demande(n_da):
    cur.execute("DELETE FROM demande_en_cours WHERE n_da = %s", (n_da,))
    conn.commit()
    return redirect("/demande")

# Transférer vers historique DA
@app.route("/transfer_da")
def transfer_da():
    cur.execute("""
        INSERT INTO historique_da (n_da, date, affectation, type_achat, reference, quantite, observation, demande_recu, etat_da)
        SELECT n_da, date, affectation, type_achat, reference, quantite, observation, demande_recu, 'livré totalement'
        FROM demande_en_cours WHERE demande_recu = TRUE
    """)
    conn.commit()
    return redirect("/historique_da")

# Afficher historique DA
@app.route("/historique_da")
def historique_da():
    cur.execute("SELECT * FROM historique_da")
    rows = cur.fetchall()
    return render_template("historique_da.html", rows=rows)

# Afficher suivi des interventions
@app.route("/suivi_interventions")
def suivi_interventions():
    cur.execute("SELECT * FROM suivi_interventions")
    rows = cur.fetchall()
    return render_template("suivi_interventions.html", rows=rows)

# Ajouter une intervention
@app.route("/add_intervention", methods=["POST"])
def add_intervention():
    date = request.form["date"]
    equipement = request.form["equipement"]
    panne = request.form["panne"]
    action = request.form["action"]
    taux_avancement = request.form["taux_avancement"]

    cur.execute("""
        INSERT INTO suivi_interventions (date, equipement, panne, action, taux_avancement)
        VALUES (%s, %s, %s, %s, %s)
    """, (date, equipement, panne, action, taux_avancement))
    conn.commit()
    return redirect("/suivi_interventions")

# Modifier une intervention
@app.route("/edit_intervention/<int:n_inter>", methods=["GET", "POST"])
def edit_intervention(n_inter):
    if request.method == "GET":
        cur.execute("SELECT * FROM suivi_interventions WHERE n_inter = %s", (n_inter,))
        row = cur.fetchone()
        return render_template("edit_intervention.html", row=row)
    else:
        date = request.form["date"]
        equipement = request.form["equipement"]
        panne = request.form["panne"]
        action = request.form["action"]
        taux_avancement = request.form["taux_avancement"]

        cur.execute("""
            UPDATE suivi_interventions
            SET date=%s, equipement=%s, panne=%s, action=%s, taux_avancement=%s
            WHERE n_inter=%s
        """, (date, equipement, panne, action, taux_avancement, n_inter))
        conn.commit()
        return redirect("/suivi_interventions")

# Supprimer une intervention
@app.route("/delete_intervention/<int:n_inter>")
def delete_intervention(n_inter):
    cur.execute("DELETE FROM suivi_interventions WHERE n_inter = %s", (n_inter,))
    conn.commit()
    return redirect("/suivi_interventions")

if __name__ == "__main__":
    app.run(debug=True)
