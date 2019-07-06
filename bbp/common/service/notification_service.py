class NotificationService:
    def __init__(self, logger, named_item_service, async_service):
        self._logger = logger
        self._named_item_service = named_item_service
        self._async_service = async_service

    def has_notification_condition(self, condition_name):
        condition_item_name = self._get_condition_item_name(condition_name)
        return self._named_item_service.has(condition_item_name)

    def get_notification_condition(self, condition_name):
        condition_item_name = self._get_condition_item_name(condition_name)
        if self.has_notification_condition(condition_name):
            condition = self._named_item_service.get(condition_item_name)
        else:
            condition = self._async_service.condition()
            self._logger.debug("created new condition {} named {}. Item name {}",
                               condition, condition_name, condition_item_name)
            self._named_item_service.set(condition_item_name, condition)
        return condition

    def notify(self, condition_name, notify_count=1):
        if not self.has_notification_condition(condition_name):
            self._logger.warn(
                "Tried to issue notification on an unregistered condition named: {}", condition_name)
            return

        condition = self.get_notification_condition(condition_name)
        if condition.locked():
            if notify_count > 0:
                self._logger.debug(
                    "on condition {} named {} going to notify up to {} observers", condition, condition_name, notify_count)
                condition.notify(notify_count)
            else:
                self._logger.debug(
                    "on condition {} named {} going to notify all observers", condition, condition_name)
                condition.notify_all()
        else:
            self._logger.warn(
                "condition {} named {} was not locked. No notification has taken place", condition, condition_name)

    def notify_all(self, condition_name):
        self.notify(condition_name, 0)

    def cancel_notification_condition(self, condition_name):
        if self.has_notification_condition(condition_name):
            self._logger.debug(
                "This condition is being cancelled. This is done by notifying all observers waiting on condition named {}.", condition_name)
            self.notify_all(condition_name)

    def _get_condition_item_name(self, condition_name):
        return f"{type(self).__name__}.{condition_name}"
