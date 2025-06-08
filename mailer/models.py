"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


from taggit.managers import TaggableManager
from common_library.db import TimestampedULIDBaseModel, UlidField


User = get_user_model()


class BadgePixelTracker(TimestampedULIDBaseModel):
    """
    Tracks a badge pixel associated with a user.
    Useful for embedding tracking pixels in emails or badges to monitor access.
    Supports tagging for flexible categorization.
    """

    title = models.CharField(
        max_length=256,
        null=True,
        help_text="Optional descriptive title for the badge tracker.",
    )
    uid = UlidField(
        verbose_name=_("uid"),
        help_text="Universally unique identifier for this badge tracker.",
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="User who owns this badge tracker."
    )
    tags = TaggableManager(help_text="Tags for categorizing this badge tracker.")

    class Meta:
        db_table = "badge-pixel-tracker"
        verbose_name = _("badge pixel tracker")
        verbose_name_plural = _("pixel trackers")
        app_label = "mailer"

    def __str__(self):
        return f"Badge Pixel Tracker {self.pk} - {self.title or 'Untitled'}"


class BadgePixelTrackerLogs(TimestampedULIDBaseModel):
    """
    Stores logs for interactions with a badge pixel.
    Captures metadata such as IP address, operating system, and request headers.
    """

    badge = models.ForeignKey(
        BadgePixelTracker,
        on_delete=models.CASCADE,
        help_text="Reference to the associated badge tracker.",
    )
    os = models.CharField(max_length=256, help_text="Operating system of the client.")
    ip = models.GenericIPAddressField(help_text="IP address of the client.")
    headers = models.JSONField(help_text="Full request headers from the client.")
    user_agent = models.CharField(
        max_length=256, help_text="User agent string of the client's browser."
    )

    class Meta:
        db_table = "badge-pixel-tracker-logs"
        verbose_name = _("badge pixel tracker log")
        verbose_name_plural = _("badge pixel tracker logs")
        app_label = "mailer"

    def __str__(self):
        return f"Log for Badge {self.badge_id} - IP: {self.ip}"


class RedirectLinkTracker(TimestampedULIDBaseModel):
    """
    Represents a redirect tracking object for monitoring link usage.
    Each instance stores the destination URL and optional title metadata,
    along with ownership tied to a user.
    """

    title = models.CharField(
        max_length=256, null=True, help_text="Optional title for the redirect link."
    )
    redirect_to = models.URLField(
        null=False, help_text="The destination URL to redirect to."
    )
    uid = UlidField(verbose_name=_("uid"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="Owner of the redirect link."
    )

    class Meta:
        db_table = "redirect-link-tracker"
        verbose_name = _("redirect link tracker")
        verbose_name_plural = _("redirects tracker")
        app_label = "mailer"

    def __str__(self):
        return f"Redirect Tracker {self.pk} - {self.title or 'No Title'}"


class RedirectLinkTrackerLog(TimestampedULIDBaseModel):
    """
    Logs each access to a redirect link.
    Captures request metadata such as IP, headers, and user agent for auditing and analytics.
    """

    redirect = models.ForeignKey(
        RedirectLinkTracker,
        on_delete=models.CASCADE,
        related_name="logs",
        help_text="Reference to the redirect link being accessed.",
    )
    ip = models.GenericIPAddressField(
        help_text="IP address of the client accessing the redirect link."
    )
    os = models.CharField(max_length=256, help_text="Operating system of the client.")
    user_agent = models.CharField(
        max_length=512, help_text="User agent string of the client."
    )
    headers = models.JSONField(help_text="Complete request headers from the client.")

    class Meta:
        db_table = "redirect-link-tracker-logs"
        verbose_name = _("redirect link tracker log")
        verbose_name_plural = _("redirect link tracker logs")
        app_label = "mailer"

    def __str__(self):
        return f"Redirect Log {self.pk} for {self.redirect_id} - IP: {self.ip}"
