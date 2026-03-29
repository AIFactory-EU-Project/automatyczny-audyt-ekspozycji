<?php

namespace App\Repository;

use App\Entity\Planogram;
use App\Entity\Segment;
use App\Entity\Shop;
use App\Entity\ShopPlanogramAssignment;
use DateTime;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;
use Doctrine\ORM\NonUniqueResultException;
use Doctrine\ORM\NoResultException;

/**
 * @method ShopPlanogramAssignment|null find($id, $lockMode = null, $lockVersion = null)
 * @method ShopPlanogramAssignment|null findOneBy(array $criteria, array $orderBy = null)
 * @method ShopPlanogramAssignment[]    findAll()
 * @method ShopPlanogramAssignment[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class ShopPlanogramAssignmentRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, ShopPlanogramAssignment::class);
    }

    public function getCurrentPlanogramAssignmentByShopAndSegment(Shop $shop, Segment $segment): ?ShopPlanogramAssignment
    {
        $timeNow = new DateTime();
        $shopId = $shop->getId();
        $segmentId = $segment->getId();

        $queryBuilder = $this->createQueryBuilder('p');
        $queryBuilder
            ->where('p.endDateTime > :timeNow')
            ->andWhere('p.startDateTime < :timeNow')
            ->andWhere('p.shop = :shop')
            ->andWhere('p.segment = :segment')
            ->setParameter('timeNow', $timeNow->format('Y-m-d H:i:s'))
            ->setParameter('shop', $shop)
            ->setParameter('segment', $segment)
            ->orderBy('p.id', 'DESC')
        ;

        try {
            return $queryBuilder->getQuery()->getSingleResult();
        } catch (NoResultException | NonUniqueResultException $e) {
            return null;
        }
    }
}
