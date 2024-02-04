## Интернет магазин Megano.

<b>Проект выполнялся в рамках дипломной работы с использованием Django Rest Framework, при 
уже существующем Frontend (javascript, html, css), а также с Swagger.
Реализация включала в себя полное соответствие выводам эндпойнтов swagger.
Используемая БД - стандартная DJANGO sqlite3.</b>
* Swagger.yaml находится в каталоге `diploma-frontend/swagger/swagger.yaml`
* Перечень доступных эндпойнтов можно получить по адресу: `/api/schema/swagger/`
## Приложения
* auth_custom - модели Профиля и Аватара
  * реализует регистрацию пользователя + создание профиля, смену пароля, аватара,
  аутентификацию, логаут
* catalog - модели категорий + картинок категорий
  * реализует перечень всех категорий, подкатегорий
  * перечень всех лимитных товаров
  * перечень всех сущностей модели Banners
  * перечень всех сущностей модели Sales
  * перечень всех популярных товаров
  * перечень всех товаров
  * сортировку товаров, согласно выбранного типа на сайте
* basket - модель корзины и товаров в корзине
  * реализует просмотр корзины, добавление, удаление товаров из корзины
* order - модель заказов, позволяющая создавать, просматривать заказы
* payment - модель оплаты
* tags - модель тэгов (выводит перечень тэгов)
* product - модели спецификаций, продуктов, картинок товаров, отзывы, и Sales (3 случайные карточки на главной странице)
  * просмотр деталей продукта
  * создание отзыва

|    | Пойнт                    | Метод  |
|----|--------------------------|--------|
| 1  | /api/banners/            | GET    |
| 2  | /api/basket/             | GET    |
| 3  | /api/basket/             | POST   |
| 4  | /api/basket/             | DELETE |
| 5  | /api/catalog/            | GET    |
| 6  | /api/categories/         | GET    |
| 7  | /api/order/id/           | GET    |
| 8  | /api/order/id/           | POST   |
| 9  | /api/orders/             | GET    |
| 10 | /api/orders/             | POST   |
| 11 | /api/payment-someone/    | POST   |
| 12 | /api/payment/id/         | POST   |
| 13 | /api/product/id/         | GET    |
| 14 | /api/product/id/reviews/ | POST   |
| 15 | /api/products/limited/   | GET    |
| 16 | /api/products/popular/   | GET    |
| 17 | /api/profile/            | GET    |
| 18 | /api/profile/            | POST   |
| 19 | /api/profile/avatar/     | POST   |
| 20 | /api/profile/password/   | POST   |
| 21 | /api/sales/              | GET    |
| 22 | /api/sign-in/            | POST   |
| 23 | /api/sign-out/           | POST   |
| 24 | /api/sigtn-up/           | POST   |
| 25 | /api/tags/               | GET    |