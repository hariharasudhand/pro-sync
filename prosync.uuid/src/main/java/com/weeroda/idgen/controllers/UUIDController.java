package com.weeroda.idgen.controllers;

import com.weeroda.idgen.documents.UUID;
import com.weeroda.idgen.dto.UUIDCreateDTO;
import com.weeroda.idgen.dto.UUIDUpdateDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


import java.util.List;

@RestController
@RequestMapping(value = "/api")
public class UUIDController {

    @Autowired
    private com.weeroda.idgen.services.UUIDService UUIDService;

    /* 
       For a given UUID , return UUID Object date 
    */
    @GetMapping(value = "/uuids/{id}")
    @ResponseStatus(HttpStatus.OK)
    public ResponseEntity<UUID> getUUID(@PathVariable(value = "id") String id){
        return new ResponseEntity<>(UUIDService.getUUIDById(id), HttpStatus.OK);
    }

    /* 
       For a given ORG ID , return all UUIDs
    */
    @GetMapping(value = "/uuids/all/{orgID}")
    @ResponseStatus(HttpStatus.OK)
    public ResponseEntity<List<UUID>> getAllUUID(@PathVariable(value = "orgID") long orgID){
        return new ResponseEntity<>(UUIDService.getAllUUID(orgID), HttpStatus.OK);
    }

    /* 
       For a given ORG ID & ProdID , return all UUIDs  
    */
    @GetMapping(value = "/uuids/all/{orgID}/{prodID}")
    @ResponseStatus(HttpStatus.OK)
    public ResponseEntity<List<UUID>> getAllUUID(@PathVariable(value = "orgID") long orgID,@PathVariable(value = "prodID") long prodID){
        return new ResponseEntity<>(UUIDService.getAllUUID(orgID,prodID), HttpStatus.OK);
    }

    /* 
       Generate  UUID for organization & product combination  
       TODO : break this function into two 1.generate & 2.save like Kavinesh
    */
    @PostMapping(value = "/uuids/gen/")
    @ResponseStatus(HttpStatus.OK)
    public ResponseEntity<List<UUID>> generateUUID(@RequestBody UUIDCreateDTO UUIDCreateDTO){
        return new ResponseEntity<>(UUIDService.generateUUID(UUIDCreateDTO), HttpStatus.CREATED);
    }

    /* 
       Save  UUID for organization & product combination  
       TODO : break this function into two 1.generate & 2.save like Kavinesh
    */
    @PostMapping(value = "/uuids/cre/")
    @ResponseStatus(HttpStatus.CREATED)
    public ResponseEntity<List<UUID>> createUUID(@RequestBody List<UUID> uuidList){
        return new ResponseEntity<>(UUIDService.createUUID(uuidList), HttpStatus.CREATED);
    }

    /* 
       Update a UUID's Object Data based on UUID
    */
    @PutMapping(value = "/uuids/{id}")
    @ResponseStatus(HttpStatus.OK)
    public ResponseEntity<UUID> updateUUID(@RequestBody UUIDUpdateDTO UUIDUpdateDTO, @PathVariable(value = "id") java.util.UUID id){
        return new ResponseEntity<>(UUIDService.updateUUID(UUIDUpdateDTO, id), HttpStatus.OK);
    }

    /* 
       Delete a UUID's Object based on UUID
    */
    @DeleteMapping(value = "/uuids/{id}")
    @ResponseStatus(HttpStatus.OK)
    public ResponseEntity<UUID> deleteUUID(@PathVariable(value="id") java.util.UUID id){
        return new ResponseEntity<>(UUIDService.deleteUUIDById(id), HttpStatus.OK);
    }


}
