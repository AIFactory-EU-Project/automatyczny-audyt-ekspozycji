<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Entity;

use DateTimeInterface;
use Doctrine\ORM\Mapping as ORM;
use JMS\Serializer\Annotation as Serializer;

/**
 * @ORM\MappedSuperclass()
 *
 * @Serializer\ExclusionPolicy("ALL")
 */
abstract class AbstractEntity
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue()
     * @ORM\Column(type="integer")
     */
    protected ?int $id = null;

    /**
     * @ORM\Column(type="datetime")
     */
    protected ?DateTimeInterface $createdDate;

    /**
     * @ORM\Column(type="datetime")
     */
    protected ?DateTimeInterface $updatedDate;

    /**
     * @ORM\Column(type="boolean")
     */
    protected bool $active = false;

    /**
     * @return int|null
     */
    public function getId(): ?int
    {
        return $this->id;
    }

    /**
     * @return DateTimeInterface
     */
    public function getCreatedDate(): DateTimeInterface
    {
        return $this->createdDate;
    }

    /**
     * @param DateTimeInterface $createdDate
     *
     * @return $this
     */
    public function setCreatedDate(DateTimeInterface $createdDate): self
    {
        $this->createdDate = $createdDate;

        return $this;
    }

    /**
     * @return DateTimeInterface
     */
    public function getUpdatedDate(): DateTimeInterface
    {
        return $this->updatedDate;
    }

    /**
     * @param DateTimeInterface $updatedDate
     *
     * @return $this
     */
    public function setUpdatedDate(DateTimeInterface $updatedDate): self
    {
        $this->updatedDate = $updatedDate;

        return $this;
    }

    /**
     * @return bool
     */
    public function getActive(): bool
    {
        return $this->active;
    }

    /**
     * @param bool $active
     *
     * @return $this
     */
    public function setActive(bool $active): self
    {
        $this->active = $active;

        return $this;
    }
}
