<?php
/**
 * @license AiFactory
 */

namespace App\Repository;

use App\Entity\ProductClass;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Common\Persistence\ManagerRegistry;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;

/**
 * @method ProductClass|null find($id, $lockMode = null, $lockVersion = null)
 * @method ProductClass|null findOneBy(array $criteria, array $orderBy = null)
 * @method ProductClass[]    findAll()
 * @method ProductClass[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class ProductClassRepository extends ServiceEntityRepository
{
    /**
     * ProductClassRepository constructor.
     *
     * @param ManagerRegistry $registry
     */
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, ProductClass::class);
    }

    /**
     * @param ProductClass $user
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function save(ProductClass $user): void
    {
        $this->_em->persist($user);
        $this->_em->flush();
    }
}
