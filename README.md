# Rate-Limited notification service

This project implements a notification system that sends out email notifications of various types and protects recipients from getting too many emails by implementing a rate limit algorithm.


## Project Structure

- `main.py`: Application entry point.
- `src/`:
  - `gateway/`:
    - `gateway.py`: Gateway implementation. Used to send messages.
  - `notification_service/`:
    - `notification_service.py`: Notification service implementation. Used to decide if a message must be sent based on the rate limit rules.
    - `notification_store.py` Notification store service implementation. Used to store the sent notifications information for each user and notification type.
  - `rate_limit_rules_service/`:
    - `rate_limit_rule.py`: Definition of the rate limit structure.
    - `rules_service.py` Rules service implementation. Used to evaluate if rate limit is exceeded for a user and a notification type.
    - `rules_store.py`: Rules store service implementation. Used to store the defined rate limit rules.
- `tests/`:
  - `test_notification_service.py`: Test cases for the notification service.


## How to Run the Program

```bash
python main.py
```

## How to Run the Tests

```bash
python -m unittest discover -v
```

## Some considerations

This program was designed with the purpose of demonstrating how a rate-limited system could be implemented. There are several things to consider if we want to implement the system in a real production environment:

### Storage of rate limit rules

The rate limit rules are defined in the `RuleStore` service. This is not a good practice because we would need to modify the code and redeploy the application each time we want to add or modify a rule. Also, if we do this, we won't be able to modify the rules in real time since the rules are loaded when the program starts. In a production implementation, we could consider using a database to store rules and query the database each time we want to evaluate a rule (or implement a cache to avoid overloading the database). The `RuleStore` service would be the responsible for managing that.

### Storage of the sent email timestamps

We are storing the timestamp of each sent message in a variable in memory. This does not scale because if we have millions of users, this object would become too large. Also, if the system restarts, we lose the information. If we host the system in Kubernetes with several replicas, this approach also fails because not every pod would have the same information. In a production implementation, we could use a Redis database to store the sent message timestamps. By doing that, we must also take into account a locking mechanism to make the system thread-safe. This logic would be implemented in the `NotificationStore` service.

In this implementation, we instantiate the `NotificationStore` service in `main.py and` then initialize both the `RulesService` and the `NotificationService` using that instance because otherwise they won't have the same information stored. This could be solved using the Singleton design pattern.


### Monitoring

We could also implement monitoring logic to detect any unexpected behavior, such as system errors or spam by using Grafana and Prometheus.

### Lost messages management

When a message is rejected because it reached the rate limit, we could implement a mechanism to store it until the rate limit allows the message to be sent. This could be done using a queue.
