"""Repository-local helper modules for the ACCTCLOCK research campaign.

The modules in this package are imported by the test suite and invoked by the
GitHub Actions controller. They are deliberately dependency-light: the only
third-party import is ``requests``, and it is imported lazily inside
:mod:`scripts.campaign_resume` so the controller never needs it.
"""
