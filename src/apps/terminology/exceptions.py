class CurrentVersionNotPrefetchedError(RuntimeError):
    """Raised when current_version is accessed without prefetching."""

    def __init__(self, refbook_id: int) -> None:
        super().__init__(
            f"Current version is not prefetched for refbook {refbook_id}. "
            "Call RefBook.objects.with_current_version() before accessing "
            "the current_version property."
        )
