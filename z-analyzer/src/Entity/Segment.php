<?php

namespace App\Entity;

use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity(repositoryClass="App\Repository\SegmentRepository")
 */
class Segment
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue()
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $name;

    /**
     * @ORM\Column(type="SegmentType")
     */
    private $type;

    /**
     * @ORM\OneToMany(targetEntity="App\Entity\Camera", mappedBy="segment")
     */
    private $cameras;

    /**
     * @ORM\OneToMany(targetEntity="App\Entity\ShopPlanogramAssignment", mappedBy="segment")
     */
    private $shopPlanogramAssignments;

    public function __construct()
    {
        $this->cameras = new ArrayCollection();
        $this->shopPlanogramAssignments =  new ArrayCollection();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getName(): ?string
    {
        return $this->name;
    }

    public function setName(string $name): self
    {
        $this->name = $name;

        return $this;
    }

    public function getType(): ?string
    {
        return $this->type;
    }

    public function setType(string $type): self
    {
        $this->type = $type;

        return $this;
    }

    public function getCameras(): Collection
    {
        return $this->cameras;
    }

    public function getShopPlanogramAssignments(): Collection
    {
        return $this->shopPlanogramAssignments;
    }
}
