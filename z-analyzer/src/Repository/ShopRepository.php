<?php

namespace App\Repository;

use App\Entity\Shop;
use App\Utility\DBAL\Type\SegmentType;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @method Shop|null find($id, $lockMode = null, $lockVersion = null)
 * @method Shop|null findOneBy(array $criteria, array $orderBy = null)
 * @method Shop[]    findAll()
 * @method Shop[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class ShopRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Shop::class);
    }

    public function getShopAudits(Shop $shop, string $segmentType)
    {
        $shortSegment = SegmentType::$shortChoices[$segmentType];

        $conn = $this->getEntityManager()->getConnection();
        $sql =
            "
                SELECT
                    rpa.id as id,
                    CONCAT ('" . $shortSegment . "', UPPER(LEFT(shop.city, 3)), TO_CHAR(rpa.date_time, 'YYYMMDDHH24MISS')) as name,
                    rpa.date_time as date,
                    shop.id as \"shopId\",
                    '" . $segmentType . "' as \"segmentTypeName\"
                FROM shop
                    INNER JOIN camera c on shop.id = c.shop_id
                    INNER JOIN photo p on c.id = p.camera_id
                    INNER JOIN report_photo_analysis rpa on p.id = rpa.photo_id
                    INNER JOIN segment s on c.segment_id = s.id
                WHERE 
                    s.type = '" . $segmentType . "' AND
                    shop.id = " . $shop->getId() . "
                ORDER BY rpa.date_time DESC;
            "
        ;

        $statement = $conn->prepare($sql);
        $statement->execute();

        return $statement->fetchAll();
    }
}
