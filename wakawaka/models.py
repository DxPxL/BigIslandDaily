from django.conf import settings
from django.db import models
from django.utils.translation import gettext


class WikiPage(models.Model):
    slug = models.CharField(("slug"), max_length=255)
    created = models.DateTimeField(("created"), auto_now_add=True)
    modified = models.DateTimeField(("modified"), auto_now=True)

    class Meta:
        verbose_name = ("Wiki page")
        verbose_name_plural = ("Wiki pages")
        ordering = ["slug"]

    def __str__(self) -> str:
        return self.slug

    @property
    def current(self):
        return self.revisions.latest()


class Revision(models.Model):
    page = models.ForeignKey(
        WikiPage,
        related_name="revisions",
        on_delete=models.CASCADE,
    )
    content = models.TextField(("content"))
    message = models.TextField(("change message"), blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="wakawaka_revisions",
        on_delete=models.CASCADE,
    )
    creator_ip = models.GenericIPAddressField(("creator ip"))
    created = models.DateTimeField(("created"), auto_now_add=True)
    modified = models.DateTimeField(("modified"), auto_now=True)

    class Meta:
        verbose_name = ("Revision")
        verbose_name_plural = ("Revisions")
        ordering = ["-modified"]
        get_latest_by = "modified"

    def __str__(self) -> str:
        return gettext("Revision %(created)s for %(page_slug)s") % {
            "created": self.created.strftime("%Y%m%d-%H%M"),
            "page_slug": self.page.slug,
        }
