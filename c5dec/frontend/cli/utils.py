"""Common functions used by CLI functionality."""

from c5dec import settings, common
import logging

log = common.logger(__name__)

def configure_logging(verbosity=0):
    """Configure logging using the provided verbosity level (0+)."""
    assert common.PRINT_VERBOSITY == 0
    assert common.STR_VERBOSITY == 3
    assert common.MAX_VERBOSITY == 4

    # Configure the logging level and format
    if verbosity == -1:
        level = settings.QUIET_LOGGING_LEVEL
        default_format = settings.DEFAULT_LOGGING_FORMAT
        verbose_format = settings.LEVELED_LOGGING_FORMAT
    elif verbosity == 0:
        level = settings.DEFAULT_LOGGING_LEVEL
        default_format = settings.DEFAULT_LOGGING_FORMAT
        verbose_format = settings.LEVELED_LOGGING_FORMAT
    elif verbosity == 1:
        level = settings.VERBOSE_LOGGING_LEVEL
        default_format = settings.DEFAULT_LOGGING_FORMAT
        verbose_format = settings.LEVELED_LOGGING_FORMAT
    elif verbosity == 2:
        level = settings.VERBOSE2_LOGGING_LEVEL
        default_format = verbose_format = settings.VERBOSE_LOGGING_FORMAT
    elif verbosity == 3:
        level = settings.VERBOSE3_LOGGING_LEVEL
        default_format = verbose_format = settings.VERBOSE_LOGGING_FORMAT
    else:
        level = settings.VERBOSE3_LOGGING_LEVEL
        default_format = verbose_format = settings.VERBOSE2_LOGGING_FORMAT

    # Set a custom formatter
    if not logging.root.handlers:
        logging.basicConfig(level=level)
        logging.captureWarnings(True)
        formatter = common.WarningFormatter(default_format, verbose_format)
        logging.root.handlers[0].setFormatter(formatter)

    # Warn about excessive verbosity
    if verbosity > common.MAX_VERBOSITY:
        msg = "maximum verbosity level is {}".format(common.MAX_VERBOSITY)
        logging.warning(msg)
        common.verbosity = common.MAX_VERBOSITY
    else:
        common.verbosity = verbosity


def configure_settings(args):
    """Update settings based on the command-line options."""

    # Parse common settings
    if args.no_reformat is not None:
        settings.REFORMAT = args.no_reformat is False
    if args.reorder is not None:
        settings.REORDER = args.reorder is True
    if args.no_level_check is not None:
        settings.CHECK_LEVELS = args.no_level_check is False
    if args.no_ref_check is not None:
        settings.CHECK_REF = args.no_ref_check is False
    if args.no_child_check is not None:
        settings.CHECK_CHILD_LINKS = args.no_child_check is False
    if args.strict_child_check is not None:
        settings.CHECK_CHILD_LINKS_STRICT = args.strict_child_check is True
    if args.no_suspect_check is not None:
        settings.CHECK_SUSPECT_LINKS = args.no_suspect_check is False
    if args.no_review_check is not None:
        settings.CHECK_REVIEW_STATUS = args.no_review_check is False
    if args.no_cache is not None:
        settings.CACHE_DOCUMENTS = args.no_cache is False
        settings.CACHE_ITEMS = args.no_cache is False
        settings.CACHE_PATHS = args.no_cache is False
    if args.warn_all is not None:
        settings.WARN_ALL = args.warn_all is True
    if args.error_all is not None:
        settings.ERROR_ALL = args.error_all is True

    # Parse `publish` settings
    if hasattr(args, "no_child_links") and args.no_child_links is not None:
        settings.PUBLISH_CHILD_LINKS = args.no_child_links is False
    if hasattr(args, "no_levels") and args.no_levels is not None:
        settings.PUBLISH_BODY_LEVELS = False
        settings.PUBLISH_HEADING_LEVELS = args.no_levels != "all"