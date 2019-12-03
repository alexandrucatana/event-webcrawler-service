package com.events.eventbyprice.controller;

import com.events.eventbyprice.messages.City;
import com.events.eventbyprice.messages.Event;
import com.events.eventbyprice.messages.Price;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

@RestController
public class EventController {

    Process mProcess;

    @Autowired
    private SimpMessagingTemplate template;


    public void runScript(String city) {
        Process process;
        try{
            process = Runtime.getRuntime().exec(new String[]{"script_python", "France", city, "300"});
            mProcess = process;
        }catch(Exception e) {
            System.out.println("Exception Raised" + e.toString());
        }
        InputStream stdout = mProcess.getInputStream();
        BufferedReader reader = new BufferedReader(new InputStreamReader(stdout, StandardCharsets.UTF_8));
        String line;
        try{
            while((line = reader.readLine()) != null){
                System.out.println("stdout: "+ line);
            }
        }catch(IOException e){
            System.out.println("Exception in reading output" + e.toString());
        }
    }

    @MessageMapping("/message")
    public void  eventName(City city) throws Exception {
        System.out.println(city.getCity());

        runScript(city.getCity());

        template.convertAndSend("/events/byprice",
                new Event("Hello Mastiksoul ", city.getCity())
        );
    }
}
