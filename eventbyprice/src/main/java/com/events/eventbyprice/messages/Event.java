package com.events.eventbyprice.messages;

import lombok.Getter;

public class Event {

    @Getter
    private String eventName;

    @Getter
    private String eventPrice;

    public Event() {}

    public Event(String eventName, String eventPrice) {
        this.eventName = eventName;
        this.eventPrice = eventPrice;
    }
}
