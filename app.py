from flask import Flask, render_template, request
import pickle
import numpy as np

res_df = pickle.load(open("popular.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
res = pickle.load(open("res.pkl", "rb"))
similarity_scores = pickle.load(open("similarity_scores.pkl", "rb"))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",
                           res_name=list(res_df["name"].values),
                           location=list(res_df["location"].values),
                           city=list(res_df["city"].values),
                           cuisines=list(res_df["cuisines"].values),
                           url=list(res_df["url"].values),
                           rating=list(res_df["Mean Rating"].values),
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template("recommend.html")

@app.route('/recommend_restaurants', methods=["post"])
def recommend():
    user_input = request.form.get("user_input")
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = res[res["name"] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates("name")["name"].values))
        item.extend(list(temp_df.drop_duplicates("name")["cuisines"].values))
        item.extend(list(temp_df.drop_duplicates("name")["url"].values))

        data.append(item)

    print(data)

    return render_template("recommend.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
