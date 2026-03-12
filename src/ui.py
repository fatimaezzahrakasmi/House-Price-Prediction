import flet as ft
import requests

def main(page: ft.Page):
    page.title = "House Price Predictor"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 500
    page.window_height = 650

    def send_to_server(e):
        submit_button.disabled = True
        submit_button.text = "Predicting..."
        page.update()

        try:
            # Gather the input values
            x_values = [
                bedrooms_input.value,
                bathrooms_input.value,
                floors_input.value,
                grade_input.value,
                yr_built_input.value,
                zipcode_input.value,
            ]

            # Convert values to appropriate types
            x_values = [int(x) if i in [0, 3, 4, 5] else float(x) for i, x in enumerate(x_values)]

            # Create a dictionary to store inputs
            data = {
                "bedrooms": x_values[0],
                "bathrooms": x_values[1],
                "floors": x_values[2],
                "grade": x_values[3],
                "yr_built": x_values[4],
                "zipcode": x_values[5],
            }

            # Send the request to the Flask server
            response = requests.post('http://127.0.0.1:5000/predict', json=data)
            response.raise_for_status() # Raise an exception for bad status codes
            
            result = response.json()
            if result.get('status') == 'success':
                price = result['predicted_price']
                result_label.value = f"Predicted Price: ${price:,.2f}"
                result_label.color = "green"
            else:
                result_label.value = f"Error: {result.get('error')}"
                result_label.color = "red"

        except ValueError:
            result_label.value = "Invalid input. Please enter valid numbers."
            result_label.color = "red"
        except requests.exceptions.RequestException as e:
            result_label.value = f"Error connecting to server. Is app.py running?"
            result_label.color = "red"
        except Exception as ex:
            result_label.value = f"An error occurred: {ex}"
            result_label.color = "red"
        finally:
            submit_button.disabled = False
            submit_button.text = "Predict Price"
            page.update()

    # Create text fields for input
    bedrooms_input = ft.TextField(label="Bedrooms (e.g. 3)", width=300)
    bathrooms_input = ft.TextField(label="Bathrooms (e.g. 2.5)", width=300)
    floors_input = ft.TextField(label="Floors (e.g. 1 or 2)", width=300)
    grade_input = ft.TextField(label="Grade (1-13)", width=300)
    yr_built_input = ft.TextField(label="Year Built (e.g. 1995)", width=300)
    zipcode_input = ft.TextField(label="Zipcode", width=300)

    # Submit button
    submit_button = ft.ElevatedButton("Predict Price", on_click=send_to_server, width=300, height=50)

    # Label to display the server response
    result_label = ft.Text(size=20, weight=ft.FontWeight.BOLD)

    page.add(
        ft.Column(
            [
                ft.Text("House Price Predictor", size=30, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20, color="transparent"),
                bedrooms_input,
                bathrooms_input,
                floors_input,
                grade_input,
                yr_built_input,
                zipcode_input,
                ft.Divider(height=20, color="transparent"),
                submit_button,
                ft.Divider(height=20, color="transparent"),
                result_label,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

if __name__ == '__main__':
    ft.app(target=main)
