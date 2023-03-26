from django.db.models.signals import post_migrate
from django.dispatch import Signal, receiver
from django.contrib.auth import get_user_model
from .models import SiteDetail, Review

custom_signal1 = Signal()
custom_signal2 = Signal()
custom_signal3 = Signal()
custom_signal4 = Signal()

User = get_user_model()


@receiver(post_migrate, dispatch_uid="1")
def create_site_detail(sender, **kwargs):
    site_detail = SiteDetail.objects.all()
    if not site_detail.exists():
        print("#########################")
        print("#-CREATING-SITE-DETAILS-#")
        print("#########################")
        print("  ---------------------  ")
        site_detail = SiteDetail.objects.create()
        print("########################")
        print("#-SITE-DETAILS-CREATED-#")
        print("########################\n")        
    custom_signal1.send(sender=sender)


@receiver(custom_signal1)
def create_test_users(sender, **kwargs):
    user_emails = User.objects.filter(email__startswith="test").values_list(
        "email", flat=True
    )
    test_emails = [
        "testadmin@email.com",
        "testreviewer@email.com",
        "testauctioneer@email.com",
    ]
    users = []
    count = 0
    for email in test_emails:
        if not email in user_emails:
            count += 1
            if count == 1:
                print("###############################")
                print("#-CREATING-INITIAL-TEST-USERS-#")
                print("###############################")
                print("  ---------------------------  ")

            user = User(
                first_name="John",
                last_name="Doe",
                email=email,
                password=email.split("@")[0],
            )
            users.append(user)

    User.objects.bulk_create(users)
    if len(users) > 0:
        print("##############################")
        print("#-INITIAL-TEST-USERS-CREATED-#")
        print("##############################\n")
    custom_signal2.send(sender=sender)


@receiver(custom_signal2)
def create_initial_reviews(sender, **kwargs):
    reviews = Review.objects.all()
    if not reviews.exists():
        print("############################")
        print("#-CREATING-INITIAL-REVIEWS-#")
        print("############################")
        print("  ------------------------  ")
        user = User.objects.get(email="testreviewer@email.com")
        reviews = [
            Review(
                user=user,
                show=True,
                text="Maecenas vitae porttitor neque, ac porttitor nunc. Duis venenatis lacinia libero. Nam nec augue ut nunc vulputate tincidunt at suscipit nunc.",
            )
            for index in range(3)
        ]
        Review.objects.bulk_create(reviews)
        print("###########################")
        print("#-INITIAL-REVIEWS-CREATED-#")
        print("###########################\n")
    custom_signal3.send(sender=sender)
