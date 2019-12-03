package com.events.eventbyprice.messages;

import lombok.Getter;

public class Price {
    @Getter
    private String eventPrice;

    public Price() {}

    public Price(String eventPrice) {
        this.eventPrice = eventPrice;
    }
}
