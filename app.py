from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_rooms, search_rooms, save_booking, get_rooms_by_id, get_recommendations
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Khởi tạo cơ sở dữ liệu
init_db()

@app.route('/')
def home():
    rooms = get_rooms()
    return render_template('home.html', rooms=rooms)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    recommendations = []
    if request.method == 'POST':
        criteria = {
            'name': request.form.get('name'),
            'price_min': request.form.get('price_min'),
            'price_max': request.form.get('price_max'),
            'capacity': request.form.get('capacity'),
            'type': request.form.get('type')
        }
        results = search_rooms(criteria)
        if not results:
            recommendations = get_recommendations()  # Gợi ý 3 phòng gần đúng nhất
        return render_template('search.html', results=results, recommendations=recommendations)
    return render_template('search.html', results=results, recommendations=recommendations)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        # Thu thập dữ liệu từ form
        customer_name = request.form['customer_name']
        rooms_booked = request.form['rooms_booked']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        guests = request.form['guests']
        customer_cmnd = request.form['customer_cmnd']
        customer_address = request.form['customer_address']
        customer_type = request.form['customer_type']

        # Tính toán tổng tiền và phát sinh mã đặt phòng
        room_ids = [int(id.strip()) for id in rooms_booked.split(',')]
        total_price = 0
        num_days = int(request.form.get('num_days'))

        for room_id in room_ids:
            room = get_rooms_by_id(room_id)
            if room:
                total_price += room[4] * num_days  # Giá 1 ngày * số ngày

        booking_code = random.randint(1000000000, 9999999999)

        # Lưu thông tin vào cơ sở dữ liệu
        save_booking({
            'customer_name': customer_name,
            'rooms_booked': rooms_booked,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'guests': guests,
            'customer_cmnd': customer_cmnd,
            'customer_address': customer_address,
            'customer_type': customer_type
        })

        # Trả lại kết quả ngay trên giao diện đặt phòng
        return render_template('booking.html', 
                               success=True, 
                               booking_code=booking_code, 
                               total_price=total_price,
                               rooms_booked=rooms_booked)
    return render_template('booking.html', success=False)


if __name__ == "__main__":
    init_db()  # Khởi tạo cơ sở dữ liệu
    app.run(debug=True)
