from .models import Author, Denomination

def seeder_func():
    authors = ["Washington Irving", "James Fenimore Cooper", "Ralph Waldo Emerson", "Louisa May Alcott"]
    denominations = ['1-cent', '2-cent', '3-cent', '4-cent']

    for author in authors:
        if not Author.objects.filter(name=author):
            new_author = Author(name=author)
            new_author.save()

    for denomination in denominations:
        if not Denomination.objects.filter(name=denomination):
            new_denomination = Denomination(name=denomination)
            new_denomination.save()