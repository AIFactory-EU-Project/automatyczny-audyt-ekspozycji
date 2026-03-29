<?php

namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity(repositoryClass="App\Repository\ShopPlanogramAssignmentRepository")
 */
class ShopPlanogramAssignment
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue(strategy="IDENTITY")
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Segment", inversedBy="shopPlanogramAssignments")
     * @ORM\JoinColumn(name="segment_id", referencedColumnName="id")
     */
    private $segment;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Shop", inversedBy="shopPlanogramAssignments")
     * @ORM\JoinColumn(name="shop_id", referencedColumnName="id")
     */
    private $shop;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Planogram", inversedBy="shopPlanogramAssignments")
     * @ORM\JoinColumn(name="planogram_id", referencedColumnName="id")
     */
    private $planogram;

    /**
     * @ORM\Column(type="datetime")
     */
    private $startDateTime;

    /**
     * @ORM\Column(type="datetime")
     */
    private $endDateTime;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getSegment(): ?Segment
    {
        return $this->segment;
    }

    public function setSegment(Segment $segment): self
    {
        $this->segment = $segment;

        return $this;
    }

    public function getShop(): ?Shop
    {
        return $this->shop;
    }

    public function setShop(Shop $shop): self
    {
        $this->shop = $shop;

        return $this;
    }

    public function getPlanogram(): ?Planogram
    {
        return $this->planogram;
    }

    public function setPlanogram(Planogram $planogram): self
    {
        $this->planogram = $planogram;

        return $this;
    }

    public function getStartDateTime(): ?\DateTimeInterface
    {
        return $this->startDateTime;
    }

    public function setStartDateTime(\DateTimeInterface $startDateTime): self
    {
        $this->startDateTime = $startDateTime;

        return $this;
    }

    public function getEndDateTime(): ?\DateTimeInterface
    {
        return $this->endDateTime;
    }

    public function setEndDateTime(\DateTimeInterface $endDateTime): self
    {
        $this->endDateTime = $endDateTime;

        return $this;
    }
}
