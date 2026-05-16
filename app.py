import streamlit as st
import serpapi
import pandas as pd
import matplotlib.pyplot as plt

def compare(med_name):
    params = {
        "engine": "google_shopping",
        "api_key": st.secrets["SERPAPI_KEY"],
        "q": med_name,
        "gl": "in",  # Country code (e.g., 'us' for USA, 'uk' for UK)
        "hl": "en"
    }
    search = serpapi.GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results["shopping_results"]
    return shopping_results

c1,c2 = st.columns(2)
c1.image("e_pharmacy.png", width= 200)
c2.header("E-Pharmacy Price compairsion system")

st.sidebar.title("Enter Name of Medicine:")
med_name=st.sidebar.text_input("Enter Medicine here 👇:")
number=st.sidebar.text_input("Enter numbers of options here 👇:")

medcine_comp = []
med_price = []


if med_name is not None:
    if st.sidebar.button("Price Compare"):
        shopping_results = compare(med_name)
        lowest_price = float((shopping_results[0].get('price'))[1:])
        print(lowest_price)
        lowest_price_index = 0
        st.sidebar.image(shopping_results[0].get("thumbnail"))
        for i in range(int(number)):
            current_price = float((shopping_results[i].get('price'))[1:])
            medcine_comp.append(shopping_results[i].get('source'))
            price = shopping_results[i].get('price')
            clean_price = float(
                ''.join(ch for ch in price if ch.isdigit() or ch == '.')
            )
            med_price.append(clean_price)

            # -----------------------------------------------
            st.title(f"Option{i+1}")

            c1,c2= st.columns(2)
            c1.write("Company:")
            c2.write(shopping_results[i].get('source'))

            c1.write("Title:")
            c2.write(shopping_results[i].get('title'))

            c1.write("Price:")
            c2.write(shopping_results[i].get('price'))

            url=shopping_results[i].get("link")
            c1.write("Buy link:")
            c2.markdown(f"[Buy Now]({url})")
            """---------------------------------------------------------------------------------"""
            if (current_price < lowest_price):
                lowest_price = current_price
                lowest_price_index = i

        # for best option

        st.title(f"Best Option:")

        c1, c2 = st.columns(2)
        c1.write("Company:")
        c2.write(shopping_results[lowest_price_index].get('source'))

        c1.write("Title:")
        c2.write(shopping_results[lowest_price_index].get('title'))

        c1.write("Price:")
        c2.write(shopping_results[lowest_price_index].get('price'))

        url = shopping_results[lowest_price_index].get("link")
        c1.write("Buy link:")
        c2.markdown(f"[Buy Now]({url})")

        # -----------------
        # Graph Comparision

        df = pd.DataFrame({"Company":medcine_comp, "price":med_price})
        st.title("Chart Comparison:")
        st.bar_chart(df.set_index("Company")["price"])

        fig,ax= plt.subplots()
        ax.pie(med_price, labels=medcine_comp, shadow=True)
        ax.axis('equal')
        st.pyplot(fig)
