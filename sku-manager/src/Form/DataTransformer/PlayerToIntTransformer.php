<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Form\DataTransformer;

use App\Entity\Player;
use App\Repository\PlayerRepository;
use Symfony\Component\Form\DataTransformerInterface;

class PlayerToIntTransformer implements DataTransformerInterface
{
    private PlayerRepository $repository;

    public function __construct(PlayerRepository $repository)
    {
        $this->repository = $repository;
    }

    public function transform($value)
    {
        if (!$value instanceof Player) {
            return null;
        }

        return $value->getId();
    }

    public function reverseTransform($value)
    {
        return $this->repository->find((int) $value);
    }
}
