package com.weeroda.idgen.repositories;

import java.util.List;
import com.weeroda.idgen.documents.UUID;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

public interface UUIDRepository extends MongoRepository<UUID, java.util.UUID> {

    /* @Query("{ $or: [ { '_id': $uuid }, { prod_item_uuid: ?0 } ] }")

    Couldn't get above to work,ideally there should be a way TODO check later
    for now i will just pass prod_item_uuid and deal with conditioning at
    Service - that's got to change */

    @Query("{ prod_item_uuid: ?0 }")
    public UUID findByUUID(String uuid);

    @Query("{ org_id: ?0 }")
    public List<UUID> findByOrgUUID(long orgID);


    @Query("{ $and: [ { 'org_id': ?0 }, { prod_id: ?1 } ] }")
    public List<UUID> findByProdUUID(long orgID,long prodID);
}
