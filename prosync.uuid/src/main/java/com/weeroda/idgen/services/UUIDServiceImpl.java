package com.weeroda.idgen.services;

import java.util.ArrayList;
import java.util.List;
import com.mongodb.MongoException;
import com.weeroda.idgen.documents.UUID;
import com.weeroda.idgen.dto.UUIDCreateDTO;
import com.weeroda.idgen.dto.UUIDUpdateDTO;
import com.weeroda.idgen.repositories.UUIDRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UUIDServiceImpl implements UUIDService {

    @Autowired
    private UUIDRepository UUIDRepository;

    @Override
    public UUID getUUIDById(String id) {

        if(UUIDRepository.findByUUID(id) != null){
            return UUIDRepository.findByUUID(id);
        }
        else if(UUIDRepository.findById(java.util.UUID.fromString(id)).isPresent()) {
            return UUIDRepository.findById(java.util.UUID.fromString(id)).get();
        }
        else{
            throw new MongoException("Record not Found");
        }
    }

    @Override
    public  List<UUID> generateUUID(UUIDCreateDTO uuidCreate) {

        List<UUID> uuidList = new ArrayList<UUID>();
        int ids = uuidCreate.getTotal_ids();
        for (int i=0;i<ids;i++) {

            uuidList.add(new UUID(uuidCreate.getExp_duration(), uuidCreate.getProd_id(), uuidCreate.getOrg_id(), uuidCreate.getAdded_date(), i));
        }
        return uuidList;
    }

     @Override
    public  List<UUID> createUUID(List<UUID> uuidList) {

        if (uuidList == null || uuidList.isEmpty()){
                throw new MongoException("UUID List is Empty, no action taken");
        }
        UUIDRepository.saveAll(uuidList);
        return uuidList;
    }

    @Override
    public UUID updateUUID(UUIDUpdateDTO uuidUpdateDTO, java.util.UUID id) {
        if (UUIDRepository.findById(id).isPresent()){
            UUID existingUUID = UUIDRepository.findById(id).get();

            existingUUID.setExp_duration(uuidUpdateDTO.getExp_duration());
            existingUUID.setProd_id(uuidUpdateDTO.getProd_id());
            existingUUID.setOrg_id(uuidUpdateDTO.getOrg_id());
            existingUUID.setAdded_date(uuidUpdateDTO.getAdded_date());

            return UUIDRepository.save(existingUUID);
        }
        else
            throw new MongoException("Record not found");
    }

    @Override
    public UUID deleteUUIDById(java.util.UUID id) {
        //TODO we don't do delete yet
        return null;
    }

    @Override
    public List<UUID> getAllUUID(long orgId){

        //TODO below if loops to be avoided , can be achived in a single query

        if(UUIDRepository.findByOrgUUID(orgId) != null){
                return UUIDRepository.findByOrgUUID(orgId);
        }else{
            throw new MongoException("No Record found,check the values,may be null or incorrect");
        }

    }

    @Override
    public List<UUID> getAllUUID(long orgId,long prodID){

        //TODO below if loops to be avoided , can be achived in a single query
        if(UUIDRepository.findByProdUUID(orgId, prodID) != null){
                return UUIDRepository.findByProdUUID(orgId, prodID);
        }
        else{
            throw new MongoException("No Record found,check the values,may be null or incorrect");
        }
    }
}
